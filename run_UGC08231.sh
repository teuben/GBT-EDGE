# Created by mk_runs.py
# UGC08231 [24] vlsr=2468.6
set -x
rm -rf UGC08231
./reduce.py -m mask_UGC08231_Havfield_v1.fits -g 24 UGC08231
./plots.sh UGC08231 _12CO_rebase5_smooth1.3_hanning2.fits 2468.6
