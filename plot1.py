#! /usr/bin/env python
#
#    average the spectrum of all points within a given radius of the reference pixel of the first fits file
#    all subsequent fits files are calibrated SDFITS files
#


import os, sys
import numpy as np

from astropy.io import fits
import matplotlib.pyplot as plt


hdu = fits.open(sys.argv[1])
ra_cen  = float(hdu[0].header['CRVAL1'])
dec_cen = float(hdu[0].header['CRVAL2'])
print(ra_cen,dec_cen)

plt.figure()

radius  = 30.0
edge = 64
Qxy = False

cosd = np.cos(dec_cen*np.pi/180)

do_sum = False
nsum = 0
ntot = 0

for f in sys.argv[2:]:
    hdu = fits.open(f)
    data = hdu[1].data

    ra = data['CRVAL2']
    dec = data['CRVAL3']
    spec = data['DATA']

    dx = (ra - ra_cen)*15*cosd * 3600
    dy = (dec - dec_cen) * 3600
    rad = np.sqrt(dx*dx+dy*dy)
    idx = np.where(rad<radius)
    #print(f,len(idx[0]),idx)
    nsum = nsum + len(idx[0])
    ntot = ntot + len(ra)
    if Qxy:
        if len(idx) > 0:
            plt.scatter(ra[idx],dec[idx])
    if do_sum == False:
        nchan = len(spec[0,:])
        chan = np.arange(nchan)
        dsum = np.zeros(nchan)
        print(dsum.shape)
        do_sum = True
    dsum = dsum + spec[idx].sum(axis=0)

print("Found %d/%d points within %g arcsec of %g %g" % (nsum,ntot,radius,ra_cen,dec_cen))
    
if not Qxy:
    x = chan[edge:nchan-edge] 
    y = dsum[edge:nchan-edge] / nsum * 1000
    plt.plot(x,y)
    plt.xlabel("Channel")
    plt.ylabel("Spectrum (mK)")

plt.show()
