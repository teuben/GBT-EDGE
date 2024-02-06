# Created by mk_runs.py
# UGC04258 [2, 2] vlsr=3097.7
set -x
rm -rf UGC04258
./reduce.py -m mask_UGC04258_Havfield_v1.fits -g 2 UGC04258
./plots.sh UGC04258 _12CO_rebase5_smooth1.3_hanning2.fits 3097.7
