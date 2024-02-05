# Created by mk_runs.py
# UGC04262 [2, 2, 34, 34, 37, 37] vlsr=5670.3
set -x
rm -rf UGC04262
./reduce.py -g -m mask_UGC04262_Havfield_v1.fits 2 UGC04262
./reduce.py -g -m mask_UGC04262_Havfield_v1.fits 34,37 -f 2 UGC04262
./plots.sh UGC04262 _12CO_rebase5_smooth1.3_hanning2.fits 5670.3
