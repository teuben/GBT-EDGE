#! /usr/bin/env python
#
#    average the spectrum of all points within a given radius of the reference pixel of the first fits file
#    all subsequent fits files are calibrated SDFITS files
#
#  Typical use in an EDGE galaxy directory:
#      ../plot1.py *_12CO_rebase3_smooth2_hanning2.fits *feed*fits


import os, sys
import numpy as np

from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

if len(sys.argv) == 0:
    print('Usage: %s template_cube.fits cs1.sdfits cs2.sdfits ...')
    print('     template_cube:        needs RA,DEC reference pixel and RESTFRQ')
    sys.exit(0)
    

template = sys.argv[1]
hdu = fits.open(template)
ra_cen  = float(hdu[0].header['CRVAL1'])
dec_cen = float(hdu[0].header['CRVAL2'])
restfrq = float(hdu[0].header['RESTFRQ'])
print('ra,dec,restfrq=',ra_cen,dec_cen,restfrq)
vref = float(hdu[0].header['CRVAL3'])
pref = float(hdu[0].header['CRPIX3'])
dv   = float(hdu[0].header['CDELT3'])
nv   = int(hdu[0].header['NAXIS3'])
vmin = (1-pref)*dv + vref
vmax = (nv-pref)*dv + vref
print("Vmin,max,dV=",vmin,vmax,dv)

plt.figure()

radius  = 20.0
edge    = 64
Qxy     = False
ckms    = 299792.458

cosd = np.cos(dec_cen*np.pi/180)

do_sum = False
nsum = 0
ntot = 0

for f in sys.argv[2:]:
    hdu = fits.open(f)
    data = hdu[1].data

    freq = data['CRVAL1']
    df   = data['CDELT1']
    fref = data['CRPIX1']
    ra   = data['CRVAL2']
    dec  = data['CRVAL3']
    spec = data['DATA']
    vel  = (1-freq/restfrq)*ckms
    dvel = -df/restfrq*ckms

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
        chan = (chan - fref[0])*dvel[0] + vel[0]
        dsum = np.zeros(nchan)
        print('nchan=',nchan)
        do_sum = True
    dsum = dsum + spec[idx].sum(axis=0)
    # print(vel)
    print(vel.min(), vel.max(), vel.max()-vel.min(),dvel[0])
    

print("Found %d/%d points within %g arcsec of %g %g" % (nsum,ntot,radius,ra_cen,dec_cen))
    
if not Qxy:
    x = chan[edge:nchan-edge] 
    y = dsum[edge:nchan-edge] / nsum * 1000
    ys = savgol_filter(y, 11, 1) 
    plt.plot(x,ys)
    plt.xlabel("velocity (-OBS) [km/s]")
    plt.ylabel("Spectrum [mK]")
    plt.title(template)
    plt.xlim([vmin,vmax])

plt.show()
