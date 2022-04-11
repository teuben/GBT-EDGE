from gbtpipe.ArgusCal import calscans, ZoneOfAvoidance, SpatialSpectralMask
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

def edgemask(galaxy):
    maskname = 'mask_{0}.fits'.format(galaxy)
    buildmasks(maskname, galname=galaxy, outdir='./',
               setups=['12CO'], grow_v=20, grow_xy=3)
    

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
             maskfile=galaxy+'12co.mask.fits',
             outname=filename)

    postprocess.cleansplit(filename + '.fits',
                           spectralSetup='12CO',
                           HanningLoops=1,
                           spatialSmooth=1.3,
                           CatalogFile='GBTEDGE.cat',
                           maskfile=galaxy+'.12co.mask.fits',
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

edgemask('NGC0001')
hdu = fits.open('NGC0001.12co.mask.fits')
maskstrategy=partial(SpatialSpectralMask, mask=hdu[0].data,
                     wcs=wcs.WCS(hdu[0].header),offpct=50)
#NGC 0001
calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=67,stop=101,refscans=[65,102], OffType='PCA', opacity=True, OffSelector=maskstrategy)
calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=23,stop=57,refscans=[21,58], OffType='PCA', opacity=True, OffSelector=maskstrategy)
edgegrid('NGC0001')

# # UGC 01569
# calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=117,stop=149,refscans=[115, 150],
#          OffType='PCA')
# calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=161,stop=194,refscans=[159, 195],
#          OffType='PCA')
# edgegrid('UGC01659')

# #UGC02239
# calscans('rawdata/AGBT21B_024_01/AGBT21B_024_01.raw.vegas',start=214,stop=248,refscans=[212, 249],
#          OffType='PCA')
# edgegrid('UGC02239')
