#! /usr/bin/env python
#
#    create run_GAL.sh files to reduce a GAL.  Do this for all GALs in gals.pars
#

import os
import sys
import glob
import GBTEDGE

ext = '_12CO_rebase5_smooth1.3_hanning2.fits'
debug = False

#   list of sessions where we have identified certain beams to be bad
#   look at the output of vanecal,VANE_SCAN for a list of Tsys(beam)
#   The -f flag use 0 based beams (0..15)
#      1..25   use all feeds
#      26..31  skip alltogether
#      32..    skip feed 2
#      42      skip feed 2,3,5    but 3,5 recovered later in the night and were < 1000
#      43..44  skip feed 2,12
#      45..    skip feed 2
#      55..    use all feeds
#      67      skip feed 5,6,9,10 (center 4 frosted over)

badfeedranges = [
    ([ 1,25],''),
    ([32,34],'-f 2'),   
    ([35,39],'-f 2,6'),   # not sure when beam 6 got bad
                          # session 39 doesn't exist (weather related)
    ([40,42],'-f 2'),
    ([43,44],'-f 2,12'),
    ([45,54],'-f 2'),
    ([55,66],''),
    ([67,67],'-f 5,6,9,10'),    
    ([68,99],''),
    ]
    

badfeeds = {}
for s in badfeedranges:
    for i in range(s[0][0],s[0][1]+1):
        badfeeds[i] = s[1]
#print(badfeeds.keys())
#print(badfeeds)

def tolist(a):
    """  list of integers   [1,4,5] ->  "1,4,5"
    """
    s = str(a[0])
    for a1 in a[1:]:
        s = s + ',%d' % a1
    return s

def masks(gal):
    """ find the mask name
    """
    gals = glob.glob('masks/*_%s_block*.fits' % gal)
    if len(gals) == 1:
        return gals[0].split('/')[1]
    gals = glob.glob('masks/*_%s_Hav*.fits' % gal)
    if len(gals) == 1:
        return gals[0].split('/')[1]
    gals = glob.glob('masks/*_%s_rotcur*.fits' % gal)
    if len(gals) > 0:
        print("Warning: %s will use the first of %s" % (gal,str(gals)))
        return gals[0].split('/')[1]
    print("Warning: %s has no mask file" % gal)
    return None

cat = GBTEDGE.GBTEDGE('GBTEDGE.cat')              # get the galaxy catalog


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

for gal in gals.keys():                   # loop over all observations
    if debug:
        print('GAL:',gal)
    s = gals[gal]
    g = cat.entry(gal)
    vlsr = g[2]

    if False:
        print(g,vlsr,s)
        continue
    
    fp = open("run_%s.sh" % gal, 'w')
    fp.write('# Created by mk_runs.py\n')
    fp.write('# %s %s vlsr=%s\n' % (gal,s,vlsr))
    fp.write('#  make sure you run this on a single core\n')
    fp.write('set -x\n')

    bf = {}
    for i in s:
        if i not in badfeeds.keys():
            continue
        flags = badfeeds[i]
        if flags not in bf.keys():
            bf[flags] = [i]
        else:
            if i not in bf[flags]:
                bf[flags].append(i)

    if False:
        print("BF:",gal,bf)
        continue

    m = masks(gal)
    if m == None:
        m = " "
    else:
        m = '-m %s' % m

    fp.write('rm -rf %s\n' % gal)
    for b in bf.keys():
        ss = bf[b]
        if len(b) == 0:
            cmd = './reduce.py %s -g %s %s' % (m,tolist(ss),gal)
        else:
            cmd = './reduce.py %s -g %s %s %s' % (m,tolist(ss),b,gal)
        #print('CMD',cmd)
        fp.write("%s\n" % cmd)
    fp.write('./plots.sh %s %s %s\n' % (gal,ext,vlsr))
    fp.close()



    # now produce the sessions
    sessions =  list(set(s))
    sessions.sort()
    fp = open("run_%s_sessions.sh" % gal, 'w')
    fp.write('# Created by mk_runs.py\n')
    fp.write('# %s %s vlsr=%s\n' % (gal,sessions,vlsr))
    fp.write('set -x\n')
    for s in sessions:
        if not s in badfeeds:
            continue
        bf = badfeeds[s]
        cmd = './reduce.py %s -g %d %s %s' % (m,s,bf,gal)
        fp.write('rm -rf %s\n' % gal)
        fp.write("%s\n" % cmd)
        fp.write('./plots.sh %s %s %s\n' % (gal,ext,vlsr))
        fp.write('rm -rf sessions/%s__%d\n' % (gal,s))
        fp.write('mv %s sessions/%s__%d\n' % (gal,gal,s))
    fp.close()
    
print("Wrote %d run_GAL.sh scripts from gals.pars" % len(gals))

