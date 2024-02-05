# Created by mk_runs.py
# UGC10905 [23, 24] vlsr=7696.5
set -x
rm -rf UGC10905
./reduce.py -m mask_UGC10905_Havfield_v1.fits -g 23,24 UGC10905
./plots.sh UGC10905 _12CO_rebase5_smooth1.3_hanning2.fits 7696.5
