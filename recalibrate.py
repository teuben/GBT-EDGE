#! /usr/bin/env python
#
# -- only for testing - not for production-
#
from gbtpipe.ArgusCal import calscans, ZoneOfAvoidance, SpatialMask, SpatialSpectralMask, NoMask
from gbtpipe import griddata
import glob
from degas import postprocess
from astropy.table import Table
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from functools import partial
from degas.masking import buildmasks
from astropy.wcs import wcs
from astropy.io import fits
from skimage import morphology as morph
from spectral_cube import SpectralCube
from radio_beam import Beam
from degas.masking import buildmasks

def edgemask(galaxy):
    maskname = 'mask_{0}.fits'.format(galaxy)
    buildmasks(maskname, galname=galaxy, outdir='./',
               setups=['12CO'], grow_v=50, grow_xy=2)
    
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

def edgegrid(galaxy):
    filelist = glob.glob(galaxy +'*_pol0.fits')
    filename = galaxy + '_12co'
    edgetrim = 64
    outdir='.'
    plotTimeSeries=True
    scanblorder=9  # Note these high order baselines
    posblorder=7   # Seem to work pretty well as long as mask is in good shape.


    griddata(filelist,
             startChannel=edgetrim,
             endChannel=1024-edgetrim,
             outdir='.',
             flagSpike=True, spikeThresh=5,
             flagRMS=True,  plotTimeSeries=plotTimeSeries,
             flagRipple=True, rippleThresh=1.3,
             pixPerBeam=4.0,
             rmsThresh=1.3,
             robust=True,
             blorder=scanblorder,
             plotsubdir='timeseries/',
             windowStrategy='cubemask',
             maskfile=galaxy+'.12co.mask.fits',
             outname=filename)

    postprocess.cleansplit(filename + '.fits',
                           spectralSetup='12CO',
                           HanningLoops=1,
                           spatialSmooth=1.3,
                           Vwindow=1500*u.km/u.s,
                           Vgalaxy=300*u.km/u.s,
                           # maskfile=galaxy+'.12co.mask.fits',    # erik first forgotten
                           CatalogFile='GBTEDGE.cat',
                           blorder=posblorder)
    
    s = SpectralCube.read(galaxy+'_12CO_rebase{0}_smooth1.3_hanning1.fits'.format(posblorder))
    s2 = s.convolve_to(Beam(12*u.arcsec))
    s2.write(galaxy+'_12CO_12arcsec.fits', overwrite=True)
    
    from astropy.convolution import Box1DKernel
    s3 = s2.spectral_smooth(Box1DKernel(5))
    s3 = s3[::5,:,:]
    s3.write(galaxy+'_12CO_12arcsec_smooth5.fits', overwrite=True)
    
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


galaxy = 'NGC2596'
galaxy = 'NGC0001'
maskdir = '/mnt/space/erosolow/edge/full/masks/'
maskdir = '/home/teuben/EDGE/GBT-EDGE/masks/'

maskname = maskdir + f'mask_{galaxy}_Havfield_v1.fits'
maskname = maskdir + f'mask_{galaxy}_square.fits'

# Note that masks now don't receive much dilation.  This is good for square masks.  
# Velocity range should be nice and tight.
buildmasks(maskname, galname=galaxy, outdir='./',
           setups=['12CO'], grow_v=0, grow_xy=0)

scans = getscans(galaxy)

hdu = fits.open(galaxy + '.12co.mask.fits')
mask = hdu[0].data

maskstrategy=partial(SpatialMask, mask=np.any(mask, axis=0),
                     wcs=wcs.WCS(hdu[0].header).celestial)

rawdir = '/mnt/space/erosolow/edge/full/GBTRawdata'
rawdir = '/home/teuben/EDGE/GBT-EDGE/rawdata'
for scanset in scans:
    calscans(rawdir + f'/AGBT21B_024_{scanset[0]:02d}/AGBT21B_024_{scanset[0]:02d}.raw.vegas',
             start=scanset[1], stop=scanset[2],
             refscans=scanset[3],
             opacity=True,
             OffSelector=maskstrategy,
             OffType='PCA',
             varrat=1.2,           # Newly exposed parameter for retaining info in PCA.
             drop_last_scan=True,  # Last scan in each row is weirdly noisy.  
             smoothpca=True)       # Smooth PCA coefficients in time.
edgegrid(galaxy)
