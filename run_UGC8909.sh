# Created by mk_runs.py
# UGC8909 [61, 61, 61, 61] vlsr=1578.3
set -x
rm -rf UGC8909
./reduce.py   -g 61 UGC8909
./plots.sh UGC8909 _12CO_rebase5_smooth1.3_hanning2.fits 1578.3
