#! /usr/bin/env python
#
#  Create a few moment (0,1,2) maps based on the maskmoment module
#
#  based on the notebook example/N4047_examples.ipyn (Tony Wong)
#

import os
import sys
sys.path.append('maskmoment')
import maskmoment
from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def quadplot(basename, extmask=None):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12,12))
    mom0 = fits.getdata(basename+'.mom0.fits.gz')
    ax1.imshow(mom0,origin='lower',cmap='CMRmap')
    ax1.set_title(basename+' - Moment 0',fontsize='x-large')
    mom1 = fits.getdata(basename+'.mom1.fits.gz')
    ax2.imshow(mom1,origin='lower',cmap='jet')
    ax2.set_title(basename+' - Moment 1',fontsize='x-large')
    mom2 = fits.getdata(basename+'.mom2.fits.gz')
    ax3.imshow(mom2,origin='lower',cmap='CMRmap')
    ax3.set_title(basename+' - Moment 2',fontsize='x-large')
    if extmask is None:
        mask = np.sum(fits.getdata(basename+'.mask.fits.gz'),axis=0)
    else:
        mask = np.sum(fits.getdata(extmask),axis=0)
    ax4.imshow(mask,origin='lower',cmap='CMRmap_r')
    ax4.set_title('Projected Mask',fontsize='x-large')
    plt.subplots_adjust(hspace=0.15,wspace=0.15)
    plt.savefig(basename + ".png")
    #plt.show()
    return



if __name__ == "__main__":
    ext = "_12CO_rebase3_hanning0"             # nothing
    ext = "_12CO_rebase3_hanning2"             # Alberto
    ext = "_12CO_rebase3_smooth1.3_hanning1"   # Erik
    ext = "_12CO_rebase3_smooth2_hanning2"     # Peter's QuickLook
    ext = "_12CO_rebase5_smooth1.3_hanning2"   # final?
    ext = "_12CO_rebase7_smooth1.3_hanning2"   # new 2025 final?
    print("Using extension name %s" % ext)
    
    for gal in sys.argv[1:]:
        if False:
            cube = "%s/%s%s.fits" % (gal,gal,ext)
            mout = "%s/%s" % (gal,gal)
        else:
            os.chdir(gal)
            cube = "%s%s.fits" % (gal,ext)
            mout = "%s" % (gal)
            
        # example 0:
        maskmoment.maskmoment(img_fits=cube,
                              snr_hi=4, snr_lo=2, minbeam=2, snr_lo_minch=2,
                              outname="%s.dilmsk" % mout)
        quadplot("%s.dilmsk" % mout)
        
        # example 1:
        maskmoment.maskmoment(img_fits=cube,
                              snr_hi=5, snr_lo=2, minbeam=2, nguard=[2,0],
                              outname='%s.dilmskpad' % mout)
        quadplot("%s.dilmskpad" % mout)
        
        # example 2:
        maskmoment.maskmoment(img_fits=cube,
                              snr_hi=3, snr_lo=3, fwhm=15, vsm=None, minbeam=2,
                              outname='%s.smomsk' % mout)
        quadplot("%s.smomsk" % mout)
        
        # example 3
        maskmoment.maskmoment(img_fits=cube,
                              snr_hi=4, snr_lo=2, fwhm=15, vsm=None, minbeam=2,
                              output_2d_mask=True,                   
                              outname='%s.dilsmomsk' % mout) 
        quadplot("%s.dilsmomsk" % mout)
        
        # example 4
        maskmoment.maskmoment(img_fits=cube,
                              rms_fits='%s.dilmsk.ecube.fits.gz' % gal,
                              mask_fits='%s.dilsmomsk.mask2d.fits.gz' % gal,
                              outname='%s.msk2d' % mout)
        # error: No such file or directory: 'NGC0001.msk2d.mask.fits.gz'
        # quadplot("%s.msk2d" % mout)        
        # flux comparisons
        ex0 = Table.read('%s.dilmsk.flux.csv'    % mout, format='ascii.ecsv')
        ex1 = Table.read('%s.dilmskpad.flux.csv' % mout, format='ascii.ecsv')
        ex2 = Table.read('%s.smomsk.flux.csv'    % mout, format='ascii.ecsv')
        ex3 = Table.read('%s.dilsmomsk.flux.csv' % mout, format='ascii.ecsv')
        ex4 = Table.read('%s.msk2d.flux.csv'     % mout, format='ascii.ecsv')
        fig = plt.figure(figsize=[8,5.5])
        plt.step(ex0['Velocity'],ex0['Flux'],color='r',label='dilmsk')
        plt.step(ex1['Velocity'],ex1['Flux'],color='b',label='dilmskpad')
        plt.step(ex2['Velocity'],ex2['Flux'],color='g',label='smomsk')
        plt.step(ex3['Velocity'],ex3['Flux'],color='k',label='dilsmomsk')
        plt.step(ex4['Velocity'],ex4['Flux'],color='orange',label='msk2d')
        plt.legend(fontsize='large')
        plt.xlabel(ex0['Velocity'].description+' ['+str(ex0['Velocity'].unit)+']',fontsize='x-large')
        plt.ylabel(ex0['Flux'].description+' ['+str(ex0['Flux'].unit)+']',fontsize='x-large')
        if True:
            t = Table.read("../GBTEDGE.cat", format='ascii')
            idx = t['NAME'] == gal
            vlsr = t[idx]['CATVEL'][0]
            ax = plt.gca()
            fmax = ax.get_ylim()[1]
            print("VLSR=",vlsr," Fmax=",fmax)
            plt.arrow(vlsr,fmax,0.0,-0.5*fmax,
                      head_width=20, head_length=0.1*fmax,
                      length_includes_head=True, facecolor='red')
            plt.annotate('VLSR', xy=(vlsr, fmax), multialignment='center')
        plt.savefig("%s.flux.png" % mout)
        #plt.show()

        # add fancier plot just for mom0 of what should be the best "detection" map
        cmd = "../fitsplot2.py %s.dilsmomsk.mom0.fits.gz --hist" % gal
        print("CMD:",cmd)
        os.system(cmd)

        os.chdir("..")
