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
    print('Usage: %s [-s] template_cube.fits cs1.sdfits cs2.sdfits ...')
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

radius  = 6.0    # one beam
radius  = 12.0
off_x   = 0.0
off_y   = 0.0
edge    = 64
Qxy     = False
ckms    = 299792.458

cosd = np.cos(dec_cen*np.pi/180)

do_sum = False
nsum = 0
ntot = 0

# NGC0001 A side
off_x = -3.556
off_y =  1.712
# NGC0001 R side
off_x =  5.444
off_y = -2.288

# NGC0001 ctr


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

    dx = (ra - ra_cen)*15*cosd * 3600 - off_x
    dy = (dec - dec_cen) * 3600       - off_y
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
    y = dsum[edge:nchan-edge] / nsum 
    if False:
        spts = 11
        sorder = 1
        ys = savgol_filter(y, spts, sorder)
    elif True:
        bp = 10
        box = np.ones(bp)/bp
        ys = np.convolve(y, box, mode='same')
    else:
        hs = 10
        h = np.hanning(hs)
        ys = np.convolve(y, h, mode='same')
    plt.plot(x,ys*1000)
    plt.xlabel("velocity (-OBS) [km/s]")
    plt.ylabel("Spectrum [mK]")
    plt.title(template)
    if vmin < vmax:
        plt.xlim([vmin,vmax])
    else:
        plt.xlim([vmax,vmin])

    np.savetxt('plot1.tab',np.transpose([x,ys]))


plt.show()
