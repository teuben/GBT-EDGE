# Created by mk_runs.py
# UGC05396 [51] vlsr=5353.7
set -x
rm -rf UGC05396
./reduce.py   -g 51 -f 2 UGC05396
./plots.sh UGC05396 _12CO_rebase5_smooth1.3_hanning2.fits 5353.7
