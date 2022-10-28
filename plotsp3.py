#! /usr/bin/env python
#

#   this code was hacked from the GBO workshop for EDGE (teuben/sdss)
#   run plot_spectrum first, it creates plot_spectrum.txt
#   then this code. Example:
#       ./plot_spectrum.py  00:07:15.84  +27:42:29.7 20 0 0    NGC0001/NGC0001_12CO_rebase5_smooth1.3_hanning2.fits
#       ./plotsp3.py  plot_spectrum.txt -1 0 3 3000 4200 4900 6000
#   @todo merge these two codes and get a better CLI parser

#
#   GBO 20m spectra plotting - September 2021 during Single Dish Workshop
#   Only useful for HIRES OnOff data
#
#   Command line options (hardcoded)
#          plotsp1.py spectrum_file [band] [smooth] [order] [baseline_section(s)]
#
#   Plotting only the XX, since the YY has calibration issues due to a bad channel
#   This scripts assume OH in the first band, and HI in the 2nd
#   There are some horrific options in the script to flip things around
#
#   Examples of use:
#
#   ./plotsp1.py group2/Skynet_59471_M31_group2_62068_10914.A.onoff.cal.txt     0 4 -770 -600 50 2200
#   ./plotsp1.py group2/Skynet_59472_ngc628_group2_62098_10938.A.onoff.cal.txt  0 8 1600 3000  100 500 800 1500
#   ./plotsp1.py group2/Skynet_59472_ngc1530_group2_62102_10937.A.onoff.cal.txt 0 8 2000 2250 2650 3400 3600 5000
#   ./plotsp1.py group2/Skynet_59472_ngc3976_group2_62119_10949.A.onoff.cal.txt 0 8
#   ./plotsp1.py group2/Skynet_59472_ngc4565_group2_62118_10948.A.onoff.cal.txt 0 8
#   

#   Some archival M31 data with better noise:
#
#   ./plotsp1.py archive/Skynet_58945_M31_10kpc_radius_44912_54515.A.onoff.cal.txt 0 8 -2100 -800 100 1000
#   ./plotsp1.py archive/Skynet_58945_M31_center_44909_54513.A.onoff.cal.txt       0 8 -2100 -600 100 1000

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- ugly command line parsing ---------------------------------------------------------------------------

if len(sys.argv) == 1:
    print("Usage:  %s table [band] [smooth] [polynomial_order] [baseline_section(s) in km/s]"  % sys.argv[0])
    print("e.g.    %s sp.txt -1 0 3 100 1000   1300  2000" % sys.argv[0])
    sys.exit(0)

tab = sys.argv[1]

if len(sys.argv) > 2:
    do_band = int(sys.argv[2])
else:
    do_band = 3
print("BAND: ",do_band)    


if len(sys.argv) > 3:
    do_smooth = int(sys.argv[3])
else:
    do_smooth = 0
print("SMOOTH: ",do_smooth)    



if len(sys.argv) > 4:
    p_order = int(sys.argv[4])
else:
    p_order = -1
print("POLY: ",p_order)    

if len(sys.argv) > 5:
    baselines = sys.argv[5:]
    nbl = len(baselines)
    if nbl%2 != 0:
        print("Need even number of baseline sections")
        sys.exit(0)
    bl = []
    nbl = nbl // 2
    for i in range(nbl):
        vmin = float(baselines[2*i])
        vmax = float(baselines[2*i+1])
        bl.append((vmin,vmax))
    print("BASELINE sections: ",bl)
else:
    bl = []
    nbl = 0


# --- a few useful helper functions ---------------------------------------------------------------------------

keywords = {}    

def get_key(key, tab=None, verbose=False):
    """  get a keyword from the tabular spectrum.
         This needs to be initialized the first call by setting tab=
    """
    if len(keywords) == 0:
        if tab == None:
            print("Cannot setup keys without given the tab= name")
            sys.exit(0)
        lines = open(tab).readlines()
        for line in lines:
            if line[0] == '#':
                words = line[1:].split('=')
                if len(words)>1:
                    key = words[0].strip()
                    val = words[1].strip()
                    if key in keywords:
                        keywords[key].append(val)
                    else:
                        keywords[key] = [val]
        if verbose:
            print(keywords)
    if key in keywords:
        return keywords[key]
    return None

def fit_poly(x, y, p_order=1, bl = []):
    """ from array X between Xmin and Xmax fit a polynomial
    """

    if len(bl) == 0:
        p = np.poly1d(np.polyfit(x,y,p_order))
        t = x
        r = y - p(x)
    else:
        first = True
        for b in bl:
            # print('B',b)
            if first:
                m = ((x>b[0]) & (x<b[1]))
                first = False
            else:
                m = m | ((x>b[0]) & (x<b[1]))
                
        p = np.poly1d(np.polyfit(x[m],y[m],p_order))
        t = x[m]
        r = y[m] - p(x[m])
    return (p,t,r)

def diff_rms(y):
    """ take the differences between neighboring signals
    and compute their rms. this should be sqrt(2)*sigma
    if there is no  trend in the input signal, and if
    the input signal is not correlated (e.g. hanning)
    """
    #y1 = y[1:]
    #y2 = y[:-1]
    return (y[1:]-y[:-1]).std() / 1.414

def my_smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def add_spectrum(filename):
    (v,t) = np.loadtxt(filename).T
    plt.plot(v,t,label=filename)

# --- useful constants --------------------------------------------------------------------

f2ref = 1420.405751786   # MHz  - HI line 
c     = 299792.458       # km/s - speed of light

normalize = False        # deprecated


# --- start of code --------------------------------------------------------------------

(v2,zz) = np.loadtxt(tab).T
# (f1,xx1,yy1,f2,xx2,yy2) = np.loadtxt(tab).T

#get_key("FILENAME",tab)
#print("DATE_OBS:  ",get_key("DATE_OBS"))
#print("OBSERVER:  ",get_key("OBSERVER"))
#print("TSYS:      ",get_key("TSYS"))

if do_smooth > 0:
    zz = my_smooth(zz,do_smooth)

if p_order >= 0:
    (p2,t2,r2) = fit_poly(v2,zz,p_order,bl)

plt.figure()

plt.plot(v2,zz)
if p_order >= 0:
    rms2 = r2.std()
    rms3 = diff_rms(r2)
    #plt.plot(t2, p2(t2), '-', label='POLY %d' % p_order)
    plt.plot(v2, p2(v2), '-', label='POLY %d SMTH %d' % (p_order,do_smooth))
    plt.plot(t2, r2, '-', label='RMS %.3g %.3g' % (rms2, rms3))
    plt.plot([v2[0],v2[-1]], [0.0, 0.0], c='black', linewidth=2, label='baseline BAND %d' % do_band)
#    
# add_spectrum('n1530_spectrum_radio_bary.tab')
#
plt.ylabel('Power [Kelvin]')
plt.xlabel('Doppler Velocity [km/s]')
plt.title(tab)
plt.legend()
plt.savefig('plotsp1.png')
plt.show()
