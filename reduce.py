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

def getscans(gal, parfile='gals.pars'):
    scans = []
    fp = open(parfile)
    lines = fp.readlines()
    for line in lines:
        if line[0] == '#':
            continue
        try:
            w = line.split()
            if len(w) < 5:
                continue
            if gal != w[0]:
                continue
            seq = int(w[1])
            start = int(w[2])
            stop = int(w[3])
            ss = w[4].split(',')
            refscans = [int(ss[0]),int(ss[1])]
            scans.append( (seq,start,stop,refscans) )
            print('%s: found %s' % (gal,scans[-1])) 
        except:
            print('Skipping parsing bad line: ',line)
    return scans

def my_calscans(gal, scan, pid='AGBT21B_024', rawdir='rawdata'):
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
        if len(scans) > 0:
            for scan in scans:
                my_calscans(gal,scan)
            edgegrid(gal)
        else:
            print("Skipping %s: no entry found" % gal)
