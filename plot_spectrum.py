#! /usr/bin/env python
#
#  Average spectrum in a GBT data set at given (ra,dec) size and (dra,ddec)
#
#  Either a single FITS cube can be given, or one or more calibrated SDFITS files
#
#  Peter Teuben - 17-mar-2022 - Created
#                 17-oct-2022 - various updates
#                 26-oct-2022 - write out spectrum for plotsp3.py
#                 28-oct-2022 - using new nemopy.getparam


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.utils import data
from spectral_cube import SpectralCube
import astropy.units as u
from nemopy import getparam


keyval = [
    "in=???\n       input fits cube",
    "ra=\n          RA   hh:mm:ss.s (or decimal degrees) [ref pixel]",
    "dec=\n         DEC  dd:mm:ss.s (or decimal degrees) [ref pixel]",
    "size=20\n      Size of area in arcsec",
    "dra=0\n        RA offset in arcsec",
    "ddec=0\n       DEC offset in arcsec",
    "sdfits=\n      optional sdfits file(s) (not re-implemented yet)",
    "tab=\n         If given, write out spectrum here",
    "vrange=\n      Plotting range in velocity",
    "irange=\n      Plotting range in intensity",
    "blorder=-1\n   Order of baseline fits (if >= 0)   ***",
    "blregion=\n    Pairs of sections along velocity axis for baseline fit",
    "VERSION=0.2\n  29-oct-2022 PJT",
]

usage = """
plot a spectrum from a cube and/or set of sdfits files

this script...
"""

p = getparam.Param(keyval,usage)

def stats3(x):
    n = len(x)
    n1 = n//3
    n2 = 2*n1
    x1 = x[:n1]
    x2 = x[n1:n2]
    x3 = x[n2:]
    print("stats  : Showing mean/std/max in 3 sections of spectrum")
    print("stats-1: ",x1.mean(), x1.std(), x1.max())
    print("stats-2: ",x2.mean(), x2.std(), x2.max())
    print("stats-3: ",x3.mean(), x3.std(), x3.max())
    print("stats  : Warning; units are mK really")

def sexa2deci(s, scale=1.0):
    """ s is a hms/dms string   12.34 or 12:34
        returns the float value
        if it's already a float, returns "as is", no
        factor 15 conversion  (this is the FITS convention)
    """
    if s.find(':') > 0:
        dms = [float(x) for x in s.split(':')]
        if len(dms) == 2:
            dms.append(0)
        if s[0] == '-':
            sign = -1
        else:
            sign = +1
        r = abs(dms[0]) + (dms[1] + dms[2]/60.0)/60.0
        return r*scale*sign
    else:
        return float(dms)
    
if p.has("ra") and p.has("dec"):
    needr  = False
    ra0    = sexa2deci(p.get("ra"), 15.0)
    dec0   = sexa2deci(p.get("dec"))
else:
    needr  = True
    print("Using reference pixel as ra=,dec=")

size   = float(p.get("size"))
dra    = float(p.get("dra"))
ddec   = float(p.get("ddec"))


def smooth(x,window_len=11,window='hanning'):

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='same')
    return y


    
# don't change these
radmax = size / 2 /  3600.0
edge = 50
c = 299792.458

#  test if a cube
ff = p.get("in")
hdu = fits.open(ff)
if hdu[0].header['NAXIS'] > 2:      
    cube = SpectralCube.read(ff).with_spectral_unit(u.km/u.s)
    if needr:
        ra0 = hdu[0].header['CRVAL1']
        dec0 = hdu[0].header['CRVAL2']
        needr = False
    
    ds9 = 'fk5; circle(%.10f, %.10f, %g")'  % (ra0,dec0,size/2)
    print('DS9',ds9)
    spectrum = cube.subcube_from_ds9region(ds9).mean(axis=(1, 2))
    spec1 = 1000 * spectrum

    crpix3 = hdu[0].header['CRPIX3']
    crval3 = hdu[0].header['CRVAL3']
    cdelt3 = hdu[0].header['CDELT3']
    if 'RESTFRQ' in hdu[0].header:
        restfr = hdu[0].header['RESTFRQ']
    elif 'RESTFREQ' in hdu[0].header:
        restfr = hdu[0].header['RESTFREQ']        
    nchan = len(spectrum)
    chan  = np.arange(0,nchan)+1
    vrad1 = (chan-crpix3) * cdelt3 + crval3
    gal   = ff.split('_')[0]    
    gal1  = ff
    sdfits = p.get('sdfits')
else:
    spec1 = None
    sdfits = p.get('sdfits')

print("PJT",ra0,dec0)

cosd0 = np.cos(dec0*np.pi/180)
dec0  = dec0 + ddec/3600.0
ra0   = ra0 + dra/3600.0/cosd0
    

# Spectra, units are mK
# spec1 :   spectrum from a FITS cube (w/ nchan and chan)
# spec2 :   from SDFITS file(s)

spec2 = None
nspec = 0
nchan = 0

# if no cube, assume they are SDFITS file(s)

for ff in sdfits:
    hdu = fits.open(ff)
    d2 = hdu[1].data
    crpix1 = d2['CRPIX1'][0]
    crval1 = d2['CRVAL1'][0]
    cdelt1 = d2['CDELT1'][0]
    restfr = d2['RESTFREQ'][0]
    restfr = 115.2712018 * 1e9
    tsys   = d2['TSYS'][0]
    if nchan == 0:
        # first time around, find the number of channels
        nchan = len(d2['DATA'][0])
        chan  = np.arange(0,nchan) + 1
        spec2 = np.zeros(nchan)
        freq  = (chan - crpix1)  * cdelt1 + crval1
        vrad2 = (1-freq/restfr)*c
        nspec = 0
        gal   = ff.split('_')[0]
        gal2  = ff
        print("Found nchan",nchan," channels ",vrad2[1]-vrad2[0])
    ra = d2['CRVAL2']
    dec = d2['CRVAL3']
    idx2 = ra[ra==0]
    idx3 = dec[dec==0]
    rad = np.sqrt( (ra-ra0)**2 + (dec-dec0)**2)
    r2c = rad[rad<radmax]
    idx = np.where(rad<radmax)[0]
    print(ff,len(idx),tsys)
    nspec = nspec + len(idx)
    spec2 = spec2 + d2['DATA'][idx].sum(axis=0)

if nspec > 0:
    spec2 = 1000 * spec2 / nspec
    tab = "plot_spectrum.txt"
    fp = open(tab,"w")
    fp.write("# generated by ",sys.argv)
    for (v,s) in zip(vrad2[edge:-edge], spec2[edge:-edge]):
        fp.write("%g %g\n" % (v,s))
    fp.close()
    print("Wrote %s average of %d spectra from SDFITS file(s)" % (tab,nspec))

if True:
    plt.figure()
    xlim = []

    # spectrum from FITS cube
    if spec1 != None:
        plt.plot(vrad1,spec1,label=gal1)
        if p.has("vrange"):
            xlim = p.listf("vrange")
        else:
            xlim = [vrad1[0],vrad1[-1]]
        plt.plot(xlim,[0,0],c='black')
        stats3(spec1)

    # spectra from SDFITS
    if nspec > 0:
        win = 11
        spec2[3*edge] = 1500
        if win > 0:
            spec2s = smooth(spec2,win)
            y = spec2s[edge:-edge]
            x=vrad2[:len(y)]
            plt.plot(x,y,label=gal2+'s')
        else:
            plt.plot(vrad2[edge:-edge], spec2[edge:-edge],label=gal2)

        # draw black baseline at T=0
        plt.plot([vrad2[0],vrad2[-1]], [0,0], c='black')
        if len(xlim) == 0:
            xlim = [vrad2[0],vrad2[-1]]
        
    plt.xlabel('Vrad (km/s)')
    plt.ylabel('T (mK)')
    if xlim[0] < xlim[1]:
        plt.xlim(xlim)
    else:
        plt.xlim([xlim[-1],xlim[0]])
    if p.has("irange"):
        ylim = p.listf("irange")
        plt.ylim(ylim)
    plt.title('%s @ %f %f size %g"' % (gal,ra0,dec0,size))
    plt.legend()
    plt.show()
    #

if p.has('tab'):
    sp_out = p.get('tab')
    sp_data = np.squeeze(np.dstack((vrad1,spec1.value)))
    np.savetxt(sp_out,sp_data,fmt='%.4f')
    print("Written ",sp_out)

# @todo:   weight by Tsys
