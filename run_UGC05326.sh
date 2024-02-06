# Created by mk_runs.py
# UGC05326 [7, 7] vlsr=1312.6
set -x
rm -rf UGC05326
./reduce.py -m mask_UGC05326_Havfield_v1.fits -g 7 UGC05326
./plots.sh UGC05326 _12CO_rebase5_smooth1.3_hanning2.fits 1312.6
