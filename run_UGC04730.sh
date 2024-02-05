# Created by mk_runs.py
# UGC04730 [5, 5, 8, 8, 33, 33, 34, 34] vlsr=3268.3
set -x
rm -rf UGC04730
./reduce.py -g -m mask_UGC04730_Havfield_v1.fits 5,8 UGC04730
./reduce.py -g -m mask_UGC04730_Havfield_v1.fits 33,34 -f 2 UGC04730
./plots.sh UGC04730 _12CO_rebase5_smooth1.3_hanning2.fits 3268.3
