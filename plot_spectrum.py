#! /usr/bin/env python
#
#  Average spectrum in a GBT data set at given (ra,dec) size and (dra,ddec)
#
#  Either a single FITS cube can be given, or one or more calibrated SDFITS files
#
#  Peter Teuben - 17-mar-2022 - Created
#


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.utils import data
from spectral_cube import SpectralCube
import astropy.units as u


if len(sys.argv) < 7:
    print("Usage %s  ra(deg) dec(deg) size(asec) dra(asec) ddec(asec)   sdfitsfile(s) | fits-cube" % sys.argv[0])
    sys.exit(0)

ra0    = float(sys.argv[1])
dec0   = float(sys.argv[2])
size   = float(sys.argv[3])
dra    = float(sys.argv[4])
ddec   = float(sys.argv[5])


# don't change these
cosd0 = np.cos(dec0*np.pi/180)
dec0  = dec0 + ddec/3600.0
ra0   = ra0 + dra/3600.0/cosd0
radmax = size / 2 /  3600.0
nchan = 0
edge = 50
c = 299792.458

#  test if a cube
ff = sys.argv[6]
hdu = fits.open(ff)
if hdu[0].header['NAXIS'] > 2:      
    cube = SpectralCube.read(ff).with_spectral_unit(u.km/u.s)
    
    ds9 = 'fk5; circle(%.10f, %.10f, %g")'  % (ra0,dec0,size/2)
    print('DS9',ds9)
    spectrum = cube.subcube_from_ds9region(ds9).mean(axis=(1, 2))
    spectrum = 1000 * spectrum

    crpix3 = hdu[0].header['CRPIX3']
    crval3 = hdu[0].header['CRVAL3']
    cdelt3 = hdu[0].header['CDELT3']
    restfr = hdu[0].header['RESTFRQ']
    nchan = len(spectrum)
    chan = np.arange(0,nchan)+1
    vrad = (chan-crpix3) * cdelt3 + crval3
    
    # gal = ff.split('_')[0]
    gal = ff
    plt.figure()
    plt.plot(vrad,spectrum)
    plt.plot([vrad[0],vrad[-1]],[0,0],c='black')
    plt.xlabel('Vrad (km/s)')
    plt.ylabel('T_A* (mK)')
    plt.title('%s @ %g %g size %g"' % (gal,ra0,dec0,size))
    #plt.xlim([vlsr[-edge],vlsr[edge]])
    plt.show()

    sys.exit(0)


# if no cube, assume they are SDFITS file(s)

for ff in sys.argv[6:]:
    hdu = fits.open(ff)
    d2 = hdu[1].data
    crpix1 = d2['CRPIX1'][0]
    crval1 = d2['CRVAL1'][0]
    cdelt1 = d2['CDELT1'][0]
    restfr = d2['RESTFREQ'][0]
    restfr = 115.2712018 * 1e9
    tsys   = d2['TSYS'][0]
    if nchan == 0:
        nchan = len(d2['DATA'][0])
        chan = np.arange(0,nchan) + 1
        spec = np.zeros(nchan)
        freq = (chan - crpix1)  * cdelt1 + crval1
        vlsr = (1-freq/restfr)*c
        nspec = 0
        # gal = ff.split('_')[0]
        gal = ff
        print("Found nchan",nchan," channels ",vlsr[1]-vlsr[0])
    ra = d2['CRVAL2']
    dec = d2['CRVAL3']
    idx2 = ra[ra==0]
    idx3 = dec[dec==0]
    rad = np.sqrt( (ra-ra0)**2 + (dec-dec0)**2)
    r2c = rad[rad<radmax]
    idx = np.where(rad<radmax)[0]
    print(ff,len(idx),tsys,restfr,crval1,cdelt1,crpix1)
    nspec = nspec + len(idx)
    spec = spec + d2['DATA'][idx].sum(axis=0)
spec = 1000 * spec / nspec

tab = "plot_spectrum.txt"
fp = open(tab,"w")
for (v,s) in zip(vlsr[edge:-edge], spec[edge:-edge]):
    fp.write("%g %g\n" % (v,s))
fp.close()
print("Wrote %s average of %d spectra" % (tab,nspec))


if True:
    plt.figure()
    plt.plot(vlsr[edge:-edge], spec[edge:-edge])
    plt.plot([vlsr[0],vlsr[-1]], [0,0], c='black')
    plt.xlabel('Vrad (km/s)')
    plt.ylabel('T_A* (mK)')
    plt.title('%s @ %g %g size %g"' % (gal,ra0,dec0,size))
    plt.xlim([vlsr[-edge],vlsr[edge]])
    plt.show()



# @todo:   weight by Tsys
