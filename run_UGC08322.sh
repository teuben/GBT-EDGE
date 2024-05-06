# Created by mk_runs.py
# UGC08322 [21, 21, 41, 41, 41, 41, 54, 54] vlsr=7574.8
set -x
rm -rf UGC08322
./reduce.py -m mask_UGC08322_Havfield_v1.fits -g 21 UGC08322
./reduce.py -m mask_UGC08322_Havfield_v1.fits -g 41,54 -f 2 UGC08322
./plots.sh UGC08322 _12CO_rebase5_smooth1.3_hanning2.fits 7574.8
