#! /usr/bin/env bash
#
#  make a mask
#     typical use:
#
#     ./mk_mask.sh refmap=NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits inc=45   pa=120  vsys=4485  mask=masks/mask_NGC0001.fits
#

refmap=masks/mask@0.010_NGC0001.fits
refmap=NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits
v1=200           # max rotation curve (vmax)
r0=20            # radius where v1 (vmax)
r1=60            # edge of galaxy
inc=45      
pa=120
vsys=4485
sig=5            # measure of width of signal. will do 4 sigma
nx=128
ny=128
nz=128
cell=2           # pixel in arcsec
chan=10          # channel in km/s
mask=mask.fits   # output file

#  simple keyword=value command line parser for bash 
for arg in $*; do
  export $arg
done

if [ -z "$NEMO" ]; then
  echo This script needs NEMO
  exit 0
fi

tmp=tmp

rm -rf $tmp.* $mask

# there is a deprecated in=, or can it be used ?
ccdvel out=$tmp.d radii=0,$r0,$r1 vrot=1,1,1      inc=$inc pa=$pa size=$nx cell=$cell amp=t
ccdvel out=$tmp.v radii=0,$r0,$r1 vrot=0,$v1,$v1  inc=$inc pa=$pa size=$nx cell=$cell amp=f vsys=$vsys
ccdvel out=$tmp.s radii=0,$r0,$r1 vrot=100,100,50 inc=$inc pa=$pa size=$nx cell=$cell amp=t

velcube - $tmp.v $tmp.d zrange=${vsys}-5*${nz}:${vsys}+5*${nz} nz=$nz sigdefault=$sig |\
  ccdmath - -  'ifgt(%1,0,1,0)' |\
  ccdfits - $mask refmap=$refmap refaxis=1,2,3 crpix=$nx/2,$nx/2,$nz/2 cdelt=$cell/3600,$cell/3600,$chan 
# crval=1.8152157770653,27.70767526688,4419.5816198067
# cunit=deg,deg,km/s

# fitshead NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits  > head1
# fitshead masks/mask@0.010_NGC0001.fits  > head2

