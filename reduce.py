#! /usr/bin/env python
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
from gbtpipe.ArgusCal import calscans, ZoneOfAvoidance
from gbtpipe import griddata
import glob
from degas import postprocess
from astropy.table import Table
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from functools import partial


def edgegrid(galaxy, wildname=None ):
    if wildname == None:
        filelist = glob.glob(galaxy +'*_pol0.fits')
    else:
        filelist = glob.glob(galaxy +'*%s*_pol0.fits' % wildname)
        
    filename = galaxy + '__12CO'
    edgetrim = 64
    outdir='.'
    plotTimeSeries=True
    scanblorder=7
    posblorder=3


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
             outname=filename)

    postprocess.cleansplit(filename + '.fits',
                           spectralSetup='12CO',
                           HanningLoops=2,          # was: 1
                           spatialSmooth=2,         # was: 1.3
                           CatalogFile='../GBTEDGE.cat',
                           blorder=posblorder)
def galcenter(galaxy):
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
    """  allowed formats:
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

def my_calscans(gal, scan, pid='AGBT21B_024', rawdir='../rawdata'):
    seq      = scan[0]
    start    = scan[1]
    stop     = scan[2]
    refscans = scan[3]
    dirname  = '%s/%s_%02d/%s_%02d.raw.vegas' % (rawdir,pid,seq,pid,seq)
    calscans(dirname, start=start, stop=stop, refscans=refscans, OffType='PCA',nProc=4,opacity=True)


if __name__ == "__main__":
    do_scan = True
    wildname = None
    grabwild = False
    for gal in sys.argv[1:]:
        if grabwild:
            print("Warning: only making map with '%s'" % gal)
            wildname = gal
            grabwild = False
            continue
        if gal == '-s':
            print("Warning: skipping accumulating scans, only doing gridding")
            do_scan = False
            continue
        if gal == '-m':
            grabwild = True
            continue
        if gal == '-h':
            print("Usage: %s [-h] [-s] galaxy [galaxy ...]" % sys.argv[0])
            print("  -h      help")
            print("  -s      skip scan building (assumed you've done it before).")
            print("  -m      match this name in wildcarding for gridding.")
            print("  galaxy  galaxy name(s), e.g. NGC0001, as they appear in gals.pars")
            continue
        print("Trying galaxy %s" % gal)
        scans = getscans(gal)
        if len(scans) > 0:
            os.makedirs(gal, exist_ok=True)
            os.chdir(gal)
            if do_scan:
                for scan in scans:
                    my_calscans(gal,scan)
            edgegrid(gal, wildname)
            os.chdir('..')
        else:
            print("Skipping %s: no entry found" % gal)
