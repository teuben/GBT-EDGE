# Created by mk_runs.py
# UGC08004 [15, 15, 34] vlsr=6159.5
set -x
rm -rf UGC08004
./reduce.py -g -m mask_UGC08004_Havfield_v1.fits 15 UGC08004
./reduce.py -g -m mask_UGC08004_Havfield_v1.fits 34 -f 2 UGC08004
./plots.sh UGC08004 _12CO_rebase5_smooth1.3_hanning2.fits 6159.5
