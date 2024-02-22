# Created by mk_runs.py
# UGC08004 [15, 15, 34, 47, 47] vlsr=6159.5
set -x
rm -rf UGC08004
./reduce.py -m mask_UGC08004_Havfield_v1.fits -g 15 UGC08004
./reduce.py -m mask_UGC08004_Havfield_v1.fits -g 34,47 -f 2 UGC08004
./plots.sh UGC08004 _12CO_rebase5_smooth1.3_hanning2.fits 6159.5
