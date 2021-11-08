#! /usr/bin/env python

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


def edgegrid(galaxy):
    filelist = glob.glob(galaxy +'*_pol0.fits')
    filename = galaxy + '_12co'
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
                           HanningLoops=1,
                           spatialSmooth=1.3,
                           CatalogFile='GBTEDGE.cat',
                           blorder=posblorder)
def galcenter(galaxy):
    CatalogFile = 'GBTEDGE.cat'
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

def getscans(gal, pars='gals.pars'):
    scans = []
    scans.append( (1, 117, 148, [115,150]) )
    scans.append( (1, 24,  57, [ 21, 58]) )
    return scans

def calscans(gal, scan, pid='AGBT21B_024', rawdir='rawdata'):
    seq      = scan[0]
    start    = scan[1]
    stop     = scan[2]
    refscans = scan[3]
    dirname  = '%s/%s_%02d/%s_%02d.raw.vegas' % (rawdir,pid,seq,pid,seq)
    calscans(dirname, start=start, stop=stop, refscans=refscans, OffType='PCA')


if __name__ == "__main__":
    for gal in sys.argv[1:]:
        print("Working on galaxy %s" % gal)
        scans = getscans(gal)
        for scan in scans:
            calscans(gal,scan)
        edgegrid(cal)
        
