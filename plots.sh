set -x

# pars      # example
gal=$1      #  gal=NGC0001
ext=$2      #  ext=_12CO_rebase5_smooth1.3_hanning2.fits
vlsr=$3     #  vlsr=4485.7

cube=$gal/${gal}${ext}
slice0=51:195-50-1
slice1=1:50,195-50:195

./mmaps.py $gal
./plot_spectrum.py $cube size=10 vlsr=$vlsr savefig=$gal/plot_spectrum1.png
./plot_spectrum.py $cube size=30 vlsr=$vlsr savefig=$gal/plot_spectrum2.png
fitsccd $cube - | ccdsub - - z=$slice0 | ccdmom - - mom=-2 | ccdmath - - "%1*1000" | ccdfits - $gal/rms0.fits
fitsccd $cube - | ccdsub - - z=$slice1 | ccdmom - - mom=-2 | ccdmath - - "%1*1000" | ccdfits - $gal/rms1.fits
./fitsplot2.py $gal/rms0.fits
./fitsplot2.py $gal/rms1.fits
