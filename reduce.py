#! /usr/bin/env python
#
#  reduce a EDGE galaxy from the GBT-EDGE survey
#  all work occurs in a subdirectory of the "galaxy" name
#
#  e.g.       ./reduce.py NGC0001
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


import os, sys
import glob
import numpy as np
from functools import partial
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.wcs import wcs
from astropy.io import fits
import astropy.units as u
from gbtpipe.ArgusCal import calscans, ZoneOfAvoidance, SpatialSpectralMask
from gbtpipe import griddata
from degas import postprocess
from degas.masking import buildmasks
# from docopt import docopt

def edgemask(galaxy, maskfile=None):
    """
    based on an input mask file (0,1) this will use
    gal_12CO.fits
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
               setups=['12CO'], grow_v=20, grow_xy=3)
    # this writes a file   outdir + galname+'.12co.mask.fits'
    # but it should return that filename
    return galaxy+'.12co.mask.fits'
    
def edgegrid(galaxy, badfeed=[], maskfile=None):
    """
    maskfile     can be None, in which case no masking was done
    badfeed      a list of (0-based) feeds that should not be included
                 from the list via wildfeed
    """
    filelist = glob.glob(galaxy +'*_pol0.fits')
    for bf in badfeed:
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
    posblorder=3
    # Erik's original
    smooth_v = 1
    smooth_xy = 1.3
    # do a bit
    smooth_v = 1
    smooth_xy = 1
    # way too smooth pipeline 
    smooth_v = 3
    smooth_xy = 3
    # do nothing
    smooth_v = 0
    smooth_xy = 0
    # default quicklook pipeline 
    smooth_v = 2
    smooth_xy = 2
    # Erik's original
    smooth_v = 1
    smooth_xy = 1.3
    # Alberto's preference
    smooth_v = 2
    smooth_xy = 0
    # default quicklook pipeline 
    smooth_v = 2
    smooth_xy = 2
    
    
    griddata(filelist,
             startChannel=edgetrim,
             endChannel=1024-edgetrim,
             outdir='.',
             flagSpike=True, spikeThresh=3,
             flagRMS=True,  plotTimeSeries=plotTimeSeries,
             flagRipple=True, rippleThresh=1.2,
             pixPerBeam=4.0,
             rmsThresh=1.1,
             robust=False,
             blorder=scanblorder,
             plotsubdir='timeseries/',
             windowStrategy='simple',
             maskfile=maskfile,
             outname=filename)

    postprocess.cleansplit(filename + '.fits',
                           spectralSetup='12CO',
                           HanningLoops=smooth_v,           # was: 1
                           spatialSmooth=smooth_xy,         # was: 1.3
                           CatalogFile='../GBTEDGE.cat',
                           maskfile=maskfile,
                           blorder=posblorder)
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

def getscans(gal, parfile='gals.pars'):
    """

    allowed formats:
       GAL  SEQ  START  STOP  REF1,REF2
       GAL  SEQ  START  STOP               #  cheating: REF1=START-2  REF2=STOP+1
    """
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
            if len(w) ==4:
                refscans = [start-2, stop+1]
            else:
                ss = w[4].split(',')
                refscans = [int(ss[0]),int(ss[1])]
            scans.append( (seq,start,stop,refscans) )
            print('%s: found %s' % (gal,scans[-1])) 
        except:
            print('Skipping parsing bad line: ',line)
    return scans

def my_calscans(gal, scan, maskstrategy, maskfile, pid='AGBT21B_024', rawdir='../rawdata'):
    """
    """
    seq      = scan[0]
    start    = scan[1]
    stop     = scan[2]
    refscans = scan[3]
    dirname  = '%s/%s_%02d/%s_%02d.raw.vegas' % (rawdir,pid,seq,pid,seq)
    if maskstrategy == None:
        calscans(dirname, start=start, stop=stop, refscans=refscans, OffType='PCA',nProc=4, opacity=True)
    else:
        calscans(dirname, start=start, stop=stop, refscans=refscans, OffType='PCA',nProc=4, opacity=True, OffSelector=maskstrategy)


def main(args):    
    """
    parse arguments (@todo use parseargs) and execute pipeline
    """
    do_scan = True
    do_mask = False
    badfeed = []
    grabwild = False
    grabmask = False
    do_seed = False
    mask2   = None
    for gal in args:
        if grabwild:
            print("Warning: removing feeds '%s'" % gal)
            badfeed =  [int(x) for x in gal.split(',')]
            grabwild = False
            print("badfeeds",badfeed)
            continue
        if grabmask:
            mask2 = gal
            print("Warning: using mask '%s'" % mask2)
            grabmask = False
            continue
        if gal == '-s':
            print("Warning: skipping accumulating scans, only doing gridding")
            do_scan = False
            continue
        if gal == '-f':
            grabwild = True
            continue
        if gal == '-M':
            do_mask = True
            continue
        if gal == '-m':
            grabmask = True
            do_mask = True
            continue
        if gal == '-h':
            print("Usage: %s [-h] [-s] [-M] [-m mfile] [-f f1,f2,...] galaxy [galaxy ...]" % sys.argv[0])
            print("  -h        help")
            print("  -s        skip scan building (assumed you've done it before).")
            print("  -f        comma separated list of bad feeds (0-based numbers)")
            print("  -M        add masking (needs special masks/mask_GAL.fits file)")
            print("  -m mfile  use masking file and deeper GAL/MASK/<results>")
            print("  galaxy  galaxy name(s), e.g. NGC0001, as they appear in gals.pars")
            continue

        if do_seed:
            # this doesn't seem to work
            print("Warning: fixed seed=123 for reproducable cubes")
            np.random.seed(123)

        print("Trying galaxy %s" % gal)
        scans = getscans(gal)
        if len(scans) > 0:
            os.makedirs(gal, exist_ok=True)
            os.chdir(gal)
            if do_mask:
                maskfile = edgemask(gal, mask2)               # make mask file
                print("Using mask from %s" % maskfile)
                hdu = fits.open(maskfile)
                maskstrategy=partial(SpatialSpectralMask, mask=hdu[0].data, wcs=wcs.WCS(hdu[0].header), offpct=50)
            else:
                maskstrategy = None
                maskfile = None
            if do_scan:
                for scan in scans:
                    my_calscans(gal, scan, maskstrategy, maskfile)
            edgegrid(gal, badfeed, maskfile)
            os.chdir('..')
        else:
            print("Skipping %s: no entry found in gals.pars" % gal)


if __name__ == "__main__":
    main(sys.argv[1:])
            
