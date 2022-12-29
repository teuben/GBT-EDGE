#! /usr/bin/env python
#
#  create a README.html summary from the stats.log file
#

import os
import sys

# stats log file
slf = "stats.log"

# changing these probably means the same change is needed in other scripts as well
mmv = "dilsmomsk.mom0"
fcv = "_12CO_rebase5_smooth1.3_hanning2"


print("<html>")

print('<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>')
print("Summary of all sources (click on column name to sort by that column)")
print("<A HREF=%s>(see also %s)</A>" % (slf,slf))

print("<P>")
print("NOTE: these results are live from the pipeline and are not science ready.")
print("<UL>")
print("<LI> Galaxy FITS cube links are to the  <B>%s.fits</B> version from the pipeline" % fcv)
print("     <br> this should have an 8 arcsec beam and 15 km/s channels")
print("<LI> RMS is determined from the inner (spatial) 40% of the cube")
print("<LI> sratio, pratio, SNR are indications how much signal there is")
print("<LI> Sessions are which of the sessions used to make this summary")
print("<LI> NF is the total number of feeds used. Usually a multiple of 32 if both DEC and RA map used.")
print("<LI> mom0 image is from MaskMoment's <B>%s.fits.gz</B> version (units K.km/s)" % mmv)
print("     <br>still taken from the flux flat cube, we don't have a noise flat cube yet. Hence the noisy edge.")
print("<LI> comments are Peter's silly comments, usually based on initial ds9 browsing")
print("     <br>- means that nothing obvious was seen")
print("<LI> if the table below is empty.... work must be in progress")
print("</UL>")

print('<table border=1 class="sortable">')
print('  <tr class="item">')

print("    <th>")
print("      Galaxy")
print("    </th>")

print("    <th>")
print("      RMS (mK)")
print("    </th>")

print("    <th>")
print("      sratio")
print("    </th>")

print("    <th>")
print("      pratio")
print("    </th>")

print("    <th>")
print("      S/N")
print("    </th>")

print("    <th>")
print("      Sessions")
print("    </th>")

print("    <th>")
print("      NF")
print("    </th>")

print("    <th>")
print("      mom0")
print("    </th>")

print("    <th>")
print("      comments")
print("    </th>")

print("  </tr>")

lines = open(slf).readlines()

for line in lines:
    line = line.strip()
    if line[0] == '#':
        # print("%s<br>" % line[1:])
        continue

    words = line.split()
    gal = words[1]
    rms = words[2]
    srat= words[3]
    prat= words[4]
    snr = words[5]
    
    ses =  "%s/sessions.log" % (gal)
    if os.path.exists(ses):
        fp = open(ses)
        ses=[]
        for line in fp.readlines():
            ses.append(int(line))
        fp.close()
        ses = list(set(ses))
        ses.sort()        
        ses = str(ses)
    else:
        ses = "TBD"

    nf  = words[6]
    
    if words[7] == "1":
        png = "%s/%s.%s.png" % (gal,gal,mmv)
    else:
        png = 0
    comm= words[8]
        
  
    print('  <tr class="item">')
    
    print("    <td>")
    fits = "%s/%s%s.fits" % (gal,gal,fcv)
    print("    <A HREF=%s>%s</A>" % (fits,gal))
    print("    </td>")

    print("    <td>")
    print("     %s" % rms)
    print("    </td>")

    print("    <td>")
    print("     %s" % srat)
    print("    </td>")

    print("    <td>")
    print("     %s" % prat)
    print("    </td>")

    print("    <td>")
    print("     %s" % snr)
    print("    </td>")

    print("    <td>")
    print("     %s" % ses)
    print("    </td>")

    print("    <td>")
    print("     %s" % nf)
    print("    </td>")

    print("    <td>")
    if png == 0:
        print("    [pic]")
    else:
        print("       <A HREF=%s> <IMG SRC=%s height=100></A>" % (png,png))
    print("    </td>")

    
    print("    <td>")
    print("     %s" % comm)    
    print("    </td>")
    
    print("  </tr>")

print("</table>")

print("Last written on: <br>")


