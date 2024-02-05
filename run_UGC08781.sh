# Created by mk_runs.py
# UGC08781 [44] vlsr=7542.7
set -x
rm -rf UGC08781
./reduce.py -g   44 -f 2 UGC08781
./plots.sh UGC08781 _12CO_rebase5_smooth1.3_hanning2.fits 7542.7
