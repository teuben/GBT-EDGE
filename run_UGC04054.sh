# Created by mk_runs.py
# UGC04054 [11, 11, 34, 34, 37] vlsr=2040.9
set -x
rm -rf UGC04054
./reduce.py -g -m mask_UGC04054_Havfield_v1.fits 11 UGC04054
./reduce.py -g -m mask_UGC04054_Havfield_v1.fits 34,37 -f 2 UGC04054
./plots.sh UGC04054 _12CO_rebase5_smooth1.3_hanning2.fits 2040.9
