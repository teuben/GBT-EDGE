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

def edgemask(galaxy):
    maskname = 'mask_{0}.fits'.format(galaxy)
    buildmasks(maskname, galname=galaxy, outdir='./',
               setups=['12CO'], grow_v=50, grow_xy=2)
    

def edgegrid(galaxy):
    filelist = glob.glob(galaxy +'*_pol0.fits')
    filename = galaxy + '_12co'
    edgetrim = 64
    outdir='.'
    plotTimeSeries=True
    scanblorder=7
    posblorder=5


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
             windowStrategy='cubemask',
             maskfile=galaxy+'.12co.mask.fits',
             outname=filename)

    postprocess.cleansplit(filename + '.fits',
                           spectralSetup='12CO',
                           HanningLoops=1,
                           spatialSmooth=1.3,
                           Vwindow=1500*u.km/u.s,
                           CatalogFile='GBTEDGE.cat',
                           maskfile=galaxy+'.12co.mask.fits',
                           blorder=posblorder)
    
    s = SpectralCube.read(galaxy+'_12CO_rebase{0}_smooth1.3_hanning1.fits'.format(posblorder))
    s2 = s.convolve_to(Beam(12*u.arcsec))
    s2.write(galaxy+'_12CO_12arcsec.fits', overwrite=True)

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

edgemask('NGC0001')
hdu = fits.open('NGC0001.12co.mask.fits')
mask = hdu[0].data

maskstrategy=partial(SpatialMask, mask=np.any(mask, axis=0),
                     wcs=wcs.WCS(hdu[0].header).celestial)

calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=67,stop=101,refscans=[65,102], OffType='PCA', opacity=True, OffSelector=maskstrategy,
         varfrac=0.1)
calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=23,stop=57,refscans=[21,58], OffType='PCA', opacity=True, OffSelector=maskstrategy,
         varfrac=0.1)
edgegrid('NGC0001')

mask = SpectralCube.read('NGC0001.12co.mask.fits')
co = SpectralCube.read('NGC0001_12CO_rebase5_smooth1.3_hanning1.fits')
mrp = mask.with_spectral_unit(u.km/u.s, velocity_convention='radio').spectral_interpolate(co.spectral_axis)
mrpp = mrp.reproject(co.header)
apix = ((co.wcs.proj_plane_pixel_area()/u.sr).to(u.dimensionless_unscaled) * (65 * u.Mpc)**2).to(u.pc**2)
dv = np.abs(co.spectral_axis[1]-co.spectral_axis[0]).to(u.km/u.s)
Lco = np.sum(co.filled_data[mrpp.filled_data[:].value > 0]) * dv * apix
Mco = np.sum(co.filled_data[mrpp.filled_data[:].value > 0]) * dv * apix * 4.3