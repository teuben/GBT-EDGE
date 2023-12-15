#! /usr/bin/env python
#
#  create a README.html summary from the stats.log file
#

import os
import sys
import numpy as np
from datetime import datetime
from astropy.io import fits

# stats log file
slf = "stats.log"

# changing these probably means a similar change is needed in other scripts as well
mmv = "dilsmomsk.mom0"
fcv = "_12CO_rebase5_smooth1.3_hanning2"



print("<html>")

print('<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>')
print("<H1> Summary of GBT-EDGE pipeline runs </H1>")
print("<A HREF=%s>(see also %s)</A>" % (slf,slf))

print("<P>")
print("NOTE: these results are live from the <A HREF=https://github.com/teuben/GBT-EDGE>pipeline</A> and are probably not science ready.")
print("<UL>")
print("<LI> Galaxy FITS cube links are to the  <B>%s.fits</B> version from the pipeline" % fcv)
print("     <br> this should have an 8 arcsec beam and 15 km/s channels")
print("<LI> RMS is determined from the inner (spatial) 40% of the cube")
print("<LI> sratio, pratio, SNR are indications how much signal there is")
print("<LI> Sessions are which of the sessions used to make this summary")
print("     <br> all sessions 26-31 should not be used")
print("<LI> NF is the total number of feeds used. Usually a multiple of 32 if both DEC and RA map used.")
print("<LI> mom0 image is from MaskMoment's <B>%s.fits.gz</B> version (units: K.km/s)" % mmv)
print("     <br>still taken from the flux flat cube, we don't have a noise flat cube yet. Hence the noisy edge.")
print("<LI> mom0peak is the peak in the mom0 from the inner 40% of the map ")
print("<LI> pipeline run is the last time the pipeline was on this galaxy")
print("<LI> comments are Peter's silly comments, usually based on initial ds9 browsing")
print("     <br>- means that nothing obvious was seen")
print("<LI> if the table below is empty.... work must be in progress")
print("</UL>")

print("(click on a column name to toggle the sorting by that column)")

print('<table border=1 class="sortable">')
print('  <tr class="item">')


print("    <th>")
print("      #")
print("    </th>")

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
print("      mom0peak")
print("    </th>")

print("    <th>")
print("      spectrum10")
print("    </th>")

print("    <th>")
print("      spectrum30")
print("    </th>")

print("    <th>")
print("      pipeline run")
print("    </th>")


print("    <th>")
print("      comments")
print("    </th>")

print("  </tr>")

lines = open(slf).readlines()
ngal = 0

for line in lines:
    line = line.strip()
    if line[0] == '#':
        # print("%s<br>" % line[1:])
        continue

    ngal = ngal + 1

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

    # find peak in the center part of mom0 fits file
    m0f =  "%s/%s.%s.fits.gz" % (gal,gal,mmv)
    if os.path.exists(m0f):
        d1 = fits.open(m0f)[0].data
        (nx,ny) = d1.shape
        d2 = d1[nx//2-nx//5:nx//2+nx//5, ny//2-ny//5:ny//2+ny//5]
        m0p = np.nanmax(d2)
    else:
        m0p = -999

    lrt = "%s/runs.log" % (gal)
    if os.path.exists(lrt):
        fp = open(lrt)
        lines = fp.readlines()
        fp.close()
        lrt = lines[-1].strip()
    else:
        lrt = "some time ago"

            
    comm= words[8]
        
  
    print('  <tr class="item">')

    print("    <td>")
    print("     %d" % ngal)
    print("    </td>")
    
    
    print("    <td>")
    ff = "%s/%s%s.fits" % (gal,gal,fcv)
    print("    <A HREF=%s>%s</A>" % (ff,gal))
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
    print("     %.2f" % m0p)
    print("    </td>")

    png1 = "%s/plot_spectrum1.png" % gal
    print("    <td>")    
    print("       <A HREF=%s> <IMG SRC=%s height=100></A>" % (png1,png1))
    print("    </td>")    

    png2 = "%s/plot_spectrum2.png" % gal
    print("    <td>")    
    print("       <A HREF=%s> <IMG SRC=%s height=100></A>" % (png2,png2))
    print("    </td>")    
    
    print("    <td>")
    print("     %s" % lrt)
    print("    </td>")
    
    print("    <td>")
    print("     %s" % comm)    
    print("    </td>")
    
    print("  </tr>")

print("</table>")

now = datetime.now()
print("Last written on: %s" % now.strftime("%Y-%m-%dT%H:%M:%S"))



