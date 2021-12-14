#! /usr/bin/env bash
#
#  make a mask
#     good examples with detected emission:
#
#     ./mk_mask.sh refmap=NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits    mask=masks/mask_NGC0001.fits 
#     ./mk_mask.sh refmap=NGC0776/NGC0776_12CO_rebase3_smooth2_hanning2.fits    mask=masks/mask_NGC0776.fits   inc=46 pa=315 vsys=4830 v1=90
#     ./mk_mask.sh refmap=NGC2691/NGC2691_12CO_rebase3_smooth2_hanning2.fits    mask=masks/mask_NGC2691.fits   inc=40 pa=345 vsys=3950 v1=200
#     ./mk_mask.sh refmap=UGC01659/UGC01659_12CO_rebase3_smooth2_hanning2.fits  mask=masks/mask_UGC01659.fits  inc=66 pa=30  vsys=8195 v1=100
#     ./mk_mask.sh refmap=UGC02134/UGC02134_12CO_rebase3_smooth2_hanning2.fits  mask=masks/mask_UGC02134.fits  inc=65 pa=285 vsys=4510 v1=165 r1=50
#     ./mk_mask.sh refmap=UGC04245/UGC04245_12CO_rebase3_smooth2_hanning2.fits  mask=masks/mask_UGC04245.fits  inc=70 pa=110 vsys=5110 v1=190 r1=40
#
# From https://www.astro.umd.edu/~bolatto/EDGE/data/galaxy_parameters.dat
# NGC0001           1.816084  27.708082    14.0     0.324   107.60
# NGC0169           9.215034  23.990973    19.0     0.473    90.70
# NGC0776          29.977188  23.644276    21.0     0.101    41.30
# NGC2691 ???
# NGC2692         134.241714  52.065948    11.0     0.547   159.60
# NGC2693         134.246964  51.347427    23.0     0.336   158.70
# UGC01659         32.487083  16.032585    20.0     0.594    35.20
# UGC02134         39.715862  27.847286    26.0     0.602   101.80
# UGC04245        122.190956  18.194210    17.0     0.683   107.20
# 
# 
# 
# 
# 
# 



#  - the defaults here are meant for NGC0001, the first galaxy we observed, and also a pretty good detection
#  - two galaxies doesn't work yet, since this script forces vsys to be at the reference pixel

refmap=masks/mask@0.010_NGC0001.fits
refmap=NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits
v1=350           # max rotation curve (vmax)
r0=10            # radius where v1 (vmax)
r1=30            # edge of galaxy
inc=42      
pa=116
vsys=4485
sig=20           # measure of width of signal. will do 4 sigma
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

# set -x

if [ -z "$NEMO" ]; then
  echo This script needs NEMO
  exit 0
fi

tmp=tmp

rm -rf $tmp.* $mask

# 0. The Rotation Center is going to be the crval of the refmap.
#    We can't trust the vref to be close to vsys though
  ra=$(fitshead $refmap | grep CRVAL1 | awk '{print $3}')
 dec=$(fitshead $refmap | grep CRVAL2 | awk '{print $3}')
vref=$(fitshead $refmap | grep CRVAL3 | awk '{print $3}')

# 1. First make Density, Velocity and Sigma maps from 0 to r1.
# ccdvel: there is a deprecated in=, or can it be used ?
ccdvel out=$tmp.d radii=0,$r0,$r1 vrot=1,1,1      inc=$inc pa=$pa size=$nx cell=$cell amp=t
ccdvel out=$tmp.v radii=0,$r0,$r1 vrot=0,$v1,$v1  inc=$inc pa=$pa size=$nx cell=$cell amp=f vsys=$vsys
ccdvel out=$tmp.s radii=0,$r0,$r1 vrot=100,100,50 inc=$inc pa=$pa size=$nx cell=$cell amp=t

# 2. Make a cube, turn into 0/1 mask, and writing as fits
#    a bug where the Sigma map was not working, so using sigdefault
#    note the refmap is in km/s
velcube - $tmp.v $tmp.d zrange=${vsys}-5*${nz}:${vsys}+5*${nz} nz=$nz sigdefault=$sig |\
  ccdmath - -  'ifgt(%1,0,1,0)' |\
  ccdfits - $mask refmap=$refmap refaxis=1,2,3 \
          crpix=$nx/2,$nx/2,$nz/2 \
          cdelt=-$cell/3600,$cell/3600,$chan \
          crval=$ra,$dec,$vsys

# 4. Some reporting
echo RA=$ra DEC=$dec VREF=$vref VSYS=$vsys

