# Created by mk_runs.py
# UGC9837 [24, 24] vlsr=2682.9
set -x
rm -rf UGC9837
./reduce.py -m mask_UGC9837_Havfield_v1.fits -g 24 UGC9837
./plots.sh UGC9837 _12CO_rebase5_smooth1.3_hanning2.fits 2682.9
