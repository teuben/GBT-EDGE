# Created by mk_runs.py
# UGC01938 [56, 56] vlsr=6285.3
set -x
rm -rf UGC01938
./reduce.py   -g 56 UGC01938
./plots.sh UGC01938 _12CO_rebase5_smooth1.3_hanning2.fits 6285.3
