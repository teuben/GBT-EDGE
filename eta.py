#! /usr/bin/env python
#  template script written by NEMO::pytable
#
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
#from degas import postprocess


def calc_etamb(freq, derr=235, Jupiter=False):

    """
    For a given input frequency, calculate and return the eta_mb value
    for the GBT using David's equation from GBT Memo 302. 

    The equation is not included in the memo and provided by private 
    communication:
        eta_jupiter = 1.23 * eta_aperture + 0.005 * (nu - 60) - 0.00003*(nu-60)**2
    where nu is in GHz.

    It comes from a polynominal fit to nu and eta_jupiter using eta_aperture
    as a function of frequency.

    This correction assumes that our sources are approximately the
    size of Jupiter (43" diameter), which isn't a bad assumption for
    extended molecular gas.

    derr:    default rms error (in microns) for the GBT

    """
    import math
    from astropy import constants as c
    import astropy.units as u

    # surface error for GBT with optimal surface and excellent weather
    esurf = 0.0235*u.cm # cm; GBT memo 302 says 230micron = 0.0230
    esurf = (derr/10000)*u.cm # cm; GBT memo 302 says 230micron = 0.0230

    # make the input frequency into a quantity if it isn't already
    if not isinstance(freq,u.Quantity):
        if freq > 1.0e9: # freq likely in Hz
            freq = freq * u.Hz
        elif freq < 200.0: # freq likely in GHz
            freq = freq * u.GHz
        else:
            print("check units on input frequency. Should be either in GHz or Hz")
    # convert frequency to GHz to use in fit
    freq = freq.to(u.GHz)

    # calculate equivalent wavelength
    wave = freq.to(u.cm, equivalencies=u.spectral()) 

    # aperture efficiency for GBT using Ruze equation.
    # 0.71 is the aperture efficiency of the GBT at lower frequency.
    eta_a = 0.71 * math.exp(- ( 4 * math.pi * esurf / wave)**2)

    if Jupiter:
        # calculate eta_mb for a jupiter sized source via 
        # polynominal fit from GBT Memo 302.  The equation is not
        # included in the memo and provided by private communication:
        #        eta_jupiter = 1.23 * eta_aperture + 0.005 * (nu - 60) -
        #        0.00003*(nu-60)**2 
        # where nu is in GHz. This correction assumes that our sources 
        # are approximately the size of Jupiter (43" diameter)
        eta_mb = 1.23 * eta_a + 0.005*(freq.value-60) - 0.00003 * (freq.value - 60)**2
    # else calculate "small source" eta_mb.
    elif freq > 110.0*u.GHz:
        # corrected for higher freq (D.Frayer) 
        eta_mb = 1.24 * (freq.value/113)**0.8 * math.exp ( -(1.3*freq.value/113)**2 )
    elif freq > 100.0*u.GHz:
        # GBT memo 302 finds that at high frequencies the eta_mb/eta_b ratio is more like 1.45 due to a slightly larger beam size factor (1.28 instead of 1.2).
        eta_mb = 1.45 * eta_a
    else: 
        # GBT memo 302 finds that for frequencies of 86-90GHz you can use the expected theoretical ratio of 1.274
        eta_mb = 1.274 * eta_a
        
    return (eta_a, eta_mb)

       

# in microns
ee = np.linspace(100,400,101)
e1 = np.zeros(len(ee))
e2 = np.zeros(len(ee))
e3 = np.zeros(len(ee))
e4 = np.zeros(len(ee))
ff = np.linspace(105,115,101)
e5 = np.zeros(len(ff))
e6 = np.zeros(len(ff))

for i in range(len(ee)):
    e1[i],e2[i] = calc_etamb(115, ee[i])
    e3[i],e4[i] = calc_etamb(113, ee[i])  

for i in range(len(ff)):
    e5[i],e6[i] = calc_etamb(ff[i])


plt.figure(1)
plt.clf()
plt.plot(ee,e1,label='$\\eta_a$ @ 115 GHz')
plt.plot(ee,e2,label='$\\eta_{mb}$ ')
plt.plot(ee,e3,'--',label='$\\eta_a$ @ 113 GHz')
plt.plot(ee,e4,'--',label='$\\eta_{mb}$ ')
plt.vlines(235,0.05,0.35,color='black')
plt.hlines(0.12,200,350,color='black')
plt.xlabel('surface RMS ($\\mu m)$')
plt.ylabel('efficiency $\\eta$')
plt.ylim(0,0.4)
plt.title('GBT efficiencies')
plt.legend()
plt.savefig('eta1.png')
plt.show()

plt.figure(2)
plt.clf()
plt.plot(ff,e5,label='$\\eta_{a}$ ')
plt.plot(ff,e6,label='$\\eta_{mb}$ ')

plt.xlabel('freq (GHz)')
plt.ylabel('efficiency $\\eta$')
#plt.ylim(0,0.4)
plt.title('GBT efficiencies')
plt.legend()
plt.savefig('eta2.png')
plt.show()






