#! /usr/bin/env python
#
#  Plot all the positions on the sky that are part of a map
#
#  Typical use in an EDGE galaxy directory:
#      ../plot0.py  *feed*fits


import os, sys
import numpy as np

from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

if len(sys.argv) == 0:
    print('Usage: %s cs1.sdfits cs2.sdfits ...')
    sys.exit(0)
    

plt.figure()



nsum = 0
ntot = 0

Qxy = True
radius = 3600

#          testing IC1683 @ 01:22:38.86  +34:26:13.2

nf = len(sys.argv[1:])
ra  = list(range(nf))
dec = list(range(nf))

track = 'Track:NONE:TPNOCAL'         #  using AZ and EL
track = 'RALongMap:NONE:TPNOCAL'
track = 'DecLatMap:NONE:TPNOCAL'
track = 'Map'

for (f,i) in zip(sys.argv[1:], range(nf)):
    hdu = fits.open(f)
    data = hdu[1].data

    obsmode = data['OBSMODE']
    # need to select when Map is in obsmode    skip those with  'Track:NONE:TPNOCAL' 
    #print(obsmode)
    #idx = np.flatnonzero(np.core.defchararray.find(obsmode,track)==-1)
    idx = np.flatnonzero(np.core.defchararray.find(obsmode,track)!=-1)
    print(idx)
    # need to know when RA=DEC=0

    ra[i]   = data['CRVAL2'][idx]
    dec[i]  = data['CRVAL3'][idx]
    print(data['OBSMODE'][idx])
    
    
ras = 0.0
decs = 0.0
n = 0
for i in range(nf):
    ras  = ras  + ra[i].sum()
    decs = decs + dec[i].sum()
    n = n + len(ra[i])
ra_cen  = ras / n
dec_cen = decs / n
print(n,ra_cen,dec_cen)

if True:
    # for IC1683
    ra_cen = 20.6619
    dec_cen = 34.437


cosd = np.cos(dec_cen*np.pi/180)

print(n,ra_cen,dec_cen,cosd)

 
if Qxy:
    for i in range(nf):
        dx = (ra[i] - ra_cen) * cosd * 3600
        dy = (dec[i] - dec_cen) * 3600
        rad = np.sqrt(dx*dx+dy*dy)
        # print(rad)
        idx = np.where(rad < 1000)
        print(idx)
        plt.scatter(dx[idx],dy[idx])
        
    plt.xlabel("dx (arcsec)")
    plt.ylabel("dy (arcsec)")
    plt.title(sys.argv[1])

plt.show()
