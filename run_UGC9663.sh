# Created by mk_runs.py
# UGC9663 [23, 23, 24] vlsr=2555.1
set -x
rm -rf UGC9663
./reduce.py -g -m mask_UGC9663_Havfield_v1.fits 23,24 UGC9663
./plots.sh UGC9663 _12CO_rebase5_smooth1.3_hanning2.fits 2555.1
