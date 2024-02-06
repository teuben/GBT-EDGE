#! /usr/bin/env python
#
#  reduce a EDGE galaxy from the GBT-EDGE survey
#  all work occurs in a subdirectory of the "galaxy" name
#
#  e.g.       ./reduce.py [options] NGC0001 [...]
#
#  options:
#    -noweather
#    -offtype PCA
#    -nproc 4
#    -scanblorder 7
#    -posblorder 3
#    -pixperbeam 3
#    -rmsthresh 1.1
#    -hanning 2
#    -smooth 2


import os
import sys
import glob
import numpy as np
from functools import partial
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.wcs import wcs
from astropy.io import fits
import astropy.units as u
from gbtpipe.ArgusCal import calscans, ZoneOfAvoidance,SpatialMask, SpatialSpectralMask, NoMask
from gbtpipe import griddata
from degas import postprocess
from degas.masking import buildmasks
#from skimage import morphology as morph
from spectral_cube import SpectralCube
from radio_beam import Beam
import argparse

__version__ = "4-feb-2024"

def edgemask(galaxy, maskfile=None):
    """
    based on an input mask file (0,1) this will use gal_12CO.fits
    or a handpicked one if maskfile given
    """
    if maskfile == None:
        maskname = '../masks/mask_{0}.fits'.format(galaxy)
        print("Reading default mask file %s" % maskname)
    else:
        if maskfile[0] == '/':
            maskname = maskfile
        else:
            maskname = '../masks/' + maskfile
    buildmasks(maskname, galname=galaxy, outdir='./',
               setups=['12CO'], grow_v=50, grow_xy=2)
    # this writes a file   outdir + galname+'.12co.mask.fits'
    # but it should return that filename
    return galaxy+'.12co.mask.fits'
    
def edgegrid(galaxy, badfeeds=[], maskfile=None):
    """
    galaxy       our galaxy name, e.g. NGC0001
    maskfile     can be None, in which case no masking was done
    badfeeds     a list of (0-based) feeds that should not be included
                 from the list via wildfeed
    """
    filelist = glob.glob(galaxy +'*_pol0.fits')
    for bf in badfeeds:
        fl = glob.glob(galaxy +'*_feed%s_*.fits' % bf)
        n = len(filelist)
        for fli in fl:
            filelist.remove(fli)
            if len(filelist) == n:
                print("Warning, could not remove",fli)
            else:
                print("Not using ",fli)
            n = len(filelist)

    filename = galaxy + '__12CO'
    edgetrim = 64
    outdir='.'
    plotTimeSeries=True
    scanblorder=7
    posblorder=5
    if maskfile == None:
        windowStrategy='simple'
    else:
        windowStrategy='cubemask'
    # example way too smooth pipeline 
    smooth_v = 3
    smooth_xy = 3
    # do a bit
    smooth_v = 1
    smooth_xy = 1
    # do nothing
    smooth_v = 0
    smooth_xy = 0
    # Peter's quicklook pipeline 
    smooth_v = 2
    smooth_xy = 2
    # Alberto's preference
    smooth_v = 2
    smooth_xy = 0
    # Erik's original
    smooth_v = 1
    smooth_xy = 1.3
    # new trial
    smooth_v = 2
    smooth_xy = 1.3
    
    griddata(filelist,
             startChannel=edgetrim,
             endChannel=1024-edgetrim,
             outdir='.',
             flagSpike=True, spikeThresh=1.5,
             flagRMS=True,  plotTimeSeries=plotTimeSeries,
             flagRipple=True, rippleThresh=1.3,
             pixPerBeam=4.0,
             rmsThresh=1.3,
             robust=False,
             blorder=scanblorder,
             plotsubdir='timeseries/',
             windowStrategy=windowStrategy,   # 'cubemask' or 'simple'
             maskfile=maskfile,
             dtype=np.float32,
             outname=filename)

    postprocess.cleansplit(filename + '.fits',
                           spectralSetup='12CO',
                           HanningLoops=smooth_v,           # was: 1
                           spatialSmooth=smooth_xy,         # was: 1.3
                           Vwindow=1500*u.km/u.s,
                           CatalogFile='../GBTEDGE.cat',
                           maskfile=maskfile,
                           blorder=posblorder)

    # @todo - match with setting
    if False:
        s = SpectralCube.read(galaxy+'_12CO_rebase{0}_smooth1.3_hanning1.fits'.format(posblorder))
        s2 = s.convolve_to(Beam(12*u.arcsec))
        s2.write(galaxy+'_12CO_12arcsec.fits', overwrite=True)

def galcenter(galaxy):
    """
    """
    CatalogFile = '../GBTEDGE.cat'
    Catalog = Table.read(CatalogFile, format='ascii')

    match = np.zeros_like(Catalog, dtype=bool)
    galcoord = None
    for index, row in enumerate(Catalog):
        if galaxy in row['NAME']:
            match[index] = True
            MatchRow = Catalog[match]
            galcoord = SkyCoord(MatchRow['RA'],
                                MatchRow['DEC'],
                                unit=(u.hourangle, u.deg))
    return(galcoord)

def getscans(gal, select=[], parfile='gals.pars'):
    """

    allowed formats:
       GAL  SEQ  START  STOP  REF1,REF2
       GAL  SEQ  START  STOP               #  cheating: REF1=START-2  REF2=STOP+1
    """
    print("getscans: ",gal,select)
    scans = []
    fp = open(parfile)
    lines = fp.readlines()
    for line in lines:
        if line[0] == '#':
            continue
        try:
            line = line.split('#')[0]    #  removing trailing comments
            w = line.split()
            if len(w) < 4:
                continue
            if gal != w[0]:
                continue
            seq = int(w[1])
            start = int(w[2])
            stop = int(w[3])
            if len(w) == 4:
                refscans = [start-2, stop+1]
            elif len(w) == 5:
                ss = w[4].split(',')
                refscans = [int(ss[0]),int(ss[1])]
            else:
                print("Skipping long line",line.strip())
                continue
            if len(select)==0 or seq in select:
                scans.append( (seq,start,stop,refscans) )
                print('%s: found %s' % (gal,scans[-1]))
            else:
                print('%s: skipping %s' % (gal,line))
        except:
            print('Skipping bad line: ',line.strip())
    return scans

def my_calscans(gal, scan, maskstrategy, maskfile, badfeeds, pid='AGBT21B_024', rawdir='../rawdata'):
    """
    badfeeds=[]   0 based bad feeds that should not be created

    """
    seq      = scan[0]
    start    = scan[1]
    stop     = scan[2]
    refscans = scan[3]
    dirname  = '%s/%s_%02d/%s_%02d.raw.vegas' % (rawdir,pid,seq,pid,seq)
    OffType  = 'PCA'   # 'linefit'  'median'   'median2d'
    if maskstrategy == None:
        calscans(dirname, start=start, stop=stop, refscans=refscans, badfeeds=badfeeds, OffType=OffType, nProc=1, opacity=True, varfrac=0.1)
    else:
        calscans(dirname, start=start, stop=stop, refscans=refscans, badfeeds=badfeeds, OffType=OffType, nProc=1, opacity=True, OffSelector=maskstrategy, varfrac=0.1)


def main(args):    
    """
    parse arguments (@todo use parseargs) and execute pipeline
    """
    do_scan = True
    do_mask = False
    badfeeds = []
    grabwild = False
    grabmask = False
    grabseq  = False
    do_seed = False
    mask2   = None
    dryrun  = False
    seq = []
    for gal in args:
        if grabwild:
            grabwild = False
            print("Warning: removing feeds '%s'" % gal)
            badfeeds =  [int(x) for x in gal.split(',')]
            print("badfeeds",badfeeds)
            continue
        if grabmask:
            mask2 = gal
            print("Using mask '%s'" % mask2)
            grabmask = False
            continue
        if grabseq:
            grabseq = False
            print("Using seq %s" % gal)
            seq = [int(x) for x in gal.split(',')]
            print("seq", seq)
            continue
        if gal == '-s':
            print("Warning: skipping accumulating scans, only doing gridding. Affects mask")
            do_scan = False
            continue
        if gal == '-n':
            dryrun = True
            continue
        if gal == '-f':
            grabwild = True
            continue
        if gal == '-g':
            grabseq = True
            continue
        if gal == '-M':
            do_mask = True
            continue
        if gal == '-m':
            grabmask = True
            do_mask = True
            continue
        if gal == '-h':
            print("Usage: %s [-h] [-s] [-M] [-m mfile] [-f f1,f2,...] [-g g1,g2,...] galaxy" % sys.argv[0])
            print("Version: %s" % __version__)
            print("  -h        help")
            print("  -s        skip scan building (assumed you've done it before).")
            print("            if mask changed, do not use -s")
            print("  -M        add masking (needs special masks/mask_GAL.fits file)")
            print("  -m mfile  use masking file and deeper GAL/MASK/<results>")
            print("  -f f1,... comma separated list of bad feeds (0-based numbers)")
            print("  -g g1,... comma separated list of good sessions (1,2,...)  [PJT only]")
            print("  -n        dryrun - report sessions/scans found and exit")
            print("  galaxy    galaxy name(s), e.g. NGC0001, as they appear in gals.pars")
            print("            In theory multiple galaxies can be used, probably not with -m,-g,-f")
            continue

        if do_seed:
            # this doesn't seem to work
            print("Warning: fixed seed=123 for reproducable cubes")
            np.random.seed(123)

        print("Trying galaxy %s" % gal)
        scans = getscans(gal, seq)
        if dryrun:
            return
        if len(scans) > 0:
            os.makedirs(gal, exist_ok=True)
            os.chdir(gal)
            
            # keep track of sessions
            fp = open("sessions.log","a")
            for scan in scans:
                fp.write("%d\n" % scan[0])
            fp.close()
            
            # log this last pipeline run
            cmd = 'date +%Y-%m-%dT%H:%M:%S >> runs.log'
            os.system(cmd)

            if do_mask:
                maskfile = edgemask(gal, mask2)               # make mask file
                print("Using mask from %s" % maskfile)
                hdu = fits.open(maskfile)
                mask = hdu[0].data 
                #maskstrategy=partial(SpatialSpectralMask, mask=hdu[0].data, wcs=wcs.WCS(hdu[0].header), offpct=50)
                maskstrategy=partial(SpatialMask, mask=np.any(mask, axis=0), wcs=wcs.WCS(hdu[0].header).celestial)
            else:
                maskstrategy = None
                maskfile = None
            print('maskfile',maskfile)
            if do_scan:
                print("CALSCANS:")
                for scan in scans:
                    my_calscans(gal, scan, maskstrategy, maskfile, badfeeds=badfeeds)
            print("EDGEGRID:")
            edgegrid(gal, badfeeds, maskfile)
            os.chdir('..')
        else:
            print("Skipping %s: no entry found in gals.pars" % gal)


if __name__ == "__main__":
    main(sys.argv[1:])
            
