# Created by mk_runs.py
# UGC10097 [23, 23, 49, 49] vlsr=5943.7
set -x
rm -rf UGC10097
./reduce.py -m mask_UGC10097_Havfield_v1.fits -g 23 UGC10097
./reduce.py -m mask_UGC10097_Havfield_v1.fits -g 49 -f 2 UGC10097
./plots.sh UGC10097 _12CO_rebase5_smooth1.3_hanning2.fits 5943.7
