# Created by mk_runs.py
# UGC04425 [44, 44] vlsr=5816.1
set -x
rm -rf UGC04425
./reduce.py   -g 44 -f 2,12 UGC04425
./plots.sh UGC04425 _12CO_rebase5_smooth1.3_hanning2.fits 5816.1
