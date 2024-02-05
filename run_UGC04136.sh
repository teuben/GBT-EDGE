# Created by mk_runs.py
# UGC04136 [2, 2, 22, 26, 26, 33, 33, 40, 40, 40, 40] vlsr=6645.0
set -x
rm -rf UGC04136
./reduce.py -m mask_UGC04136_Havfield_v1.fits -g 2,22 UGC04136
./reduce.py -m mask_UGC04136_Havfield_v1.fits -g 33,40 -f 2 UGC04136
./plots.sh UGC04136 _12CO_rebase5_smooth1.3_hanning2.fits 6645.0
