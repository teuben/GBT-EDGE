# Created by mk_runs.py
# UGC02222 [10] vlsr=4905.1
set -x
rm -rf UGC02222
./reduce.py -m mask_UGC02222_Havfield_v1.fits -g 10 UGC02222
./plots.sh UGC02222 _12CO_rebase5_smooth1.3_hanning2.fits 4905.1
