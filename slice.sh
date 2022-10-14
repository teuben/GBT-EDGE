#! /usr/bin/env bash
#



gal=$1
zmin=$2
zmax=$3
ext=_12CO_rebase5_smooth1.3_hanning2

cd $gal

fits=${gal}${ext}.fits

if [ ! -e $fits ]; then
    echo $fits does not exist
    exit 0
fi

# output file
mom0=$gal.slice.mom0.fits

# convert fits cube to mom0
rm -f $mom0
zcat ${gal}.dilmsk.mom0.fits.gz > template.fits
fitsccd $fits - | ccdsub - - z=${zmin}:${zmax} | ccdmom - - mom=0  |  ccdfits - $mom0 fitshead=template.fits

