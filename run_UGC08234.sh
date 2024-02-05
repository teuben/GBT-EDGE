# Created by mk_runs.py
# UGC08234 [44, 44, 45, 45] vlsr=8105.8
set -x
rm -rf UGC08234
./reduce.py   -g 44,45 -f 2 UGC08234
./plots.sh UGC08234 _12CO_rebase5_smooth1.3_hanning2.fits 8105.8
