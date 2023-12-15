#! /usr/bin/env python
#
#    create run_GAL.sh files to reduce a GAL.  Do this for all GALs in gals.pars
#

import os
import sys
import glob


ext = '_12CO_rebase5_smooth1.3_hanning2.fits'

def tolist(a):
    """  list of integers 
    """
    s = str(a[0])
    for a1 in a[1:]:
        s = s + ',%d' % a1
    return s

def masks(gal):
    """ find the mask name
    """
    gals = glob.glob('masks/*_%s_Hav*.fits' % gal)
    if len(gals) == 1:
        return gals[0].split('/')[1]
    gals = glob.glob('masks/*_%s_rotcur*.fits' % gal)
    if len(gals) > 0:
        print("Warning: %s will use the first of %s" % (gal,str(gals)))
        return gals[0].split('/')[1]
    print("Warning: %s has no mask file" % gal)
    return None
    

gals = {}
lines = open('gals.pars').readlines()
for line in lines:
    if line[0] == '#': continue
    words = line.split()
    if len(words) > 2:
        gal = words[0]
        s = int(words[1])        
        if gal not in gals:
            gals[gal] = [s]
        else:
            gals[gal].append(s)

for gal in gals.keys():
    s = gals[gal]
    fp = open("run_%s.sh" % gal, 'w')
    fp.write('# Created by mk_runs.py\n')
    fp.write('# %s %s\n' % (gal,s))
    fp.write('set -x\n')
    s
    ss = []  # use all feeds
    s2 = []  # skip feed 2
    sb = []  # bad ones
    sq = []  # test if empty
    for i in s:
        if i in range(26,32):
            sb.append(i)
            continue
        if i in range(1,26):
            if not i in ss:
                ss.append(i)
            continue
        if i > 31:
            if not i in s2:
                s2.append(i)
            continue
        # should not get here
        sq.append(i)
    if len(sq) > 0:
        print("Not all sessions accounted for: ",sq)
        sys.exit(0)

    m = masks(gal)
    if m == None:
        m = " "
    else:
        m = '-m %s' % m

    fp.write('rm -rf %s\n' % gal)        
    if len(s2) == 0:
        fp.write('./reduce.py %s -g %s %s\n' % (m,tolist(ss),gal))
    else:
        fp.write('./reduce.py %s -g %s -f 2 %s\n' % (m,tolist(s2),gal))
        fp.write('rm -rf %s/*_feed2_*\n' % gal)
        fp.write('./reduce.py %s -g %s  %s\n' % (m,tolist(ss),gal))
    fp.write('./mmaps.py %s\n' % gal)
    fp.write('./plot_spectrum.py %s/%s%s size=10 savefig=%s/plot_spectrum1.png\n' % (gal,gal,ext,gal))    
    fp.write('./plot_spectrum.py %s/%s%s size=30 savefig=%s/plot_spectrum2.png\n' % (gal,gal,ext,gal))
    fp.write('fitsccd %s/%s%s - | ccdmom - - mom=-2 | ccdfits - %s/rms.fits\n' % (gal,gal,ext,gal))
    fp.write('./fitsplot2.py %s/rms.fits\n' % (gal))
    
    fp.close()
print("Wrote %d run_GAL.sh scripts" % len(gals))

# rules:
# 1..25   use all feeds
# 26..31  skip
# 32..    skip feed 2
