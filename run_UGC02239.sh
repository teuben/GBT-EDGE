# Created by mk_runs.py
# UGC02239 [1, 2, 33, 33] vlsr=4776.1
set -x
rm -rf UGC02239
./reduce.py -m mask_UGC02239_Havfield_v1.fits -g 1,2 UGC02239
./reduce.py -m mask_UGC02239_Havfield_v1.fits -g 33 -f 2 UGC02239
./plots.sh UGC02239 _12CO_rebase5_smooth1.3_hanning2.fits 4776.1
