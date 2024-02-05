# Created by mk_runs.py
# UGC08733 [17, 18] vlsr=2328.7
set -x
rm -rf UGC08733
./reduce.py -m mask_UGC08733_Havfield_v1.fits -g 17,18 UGC08733
./plots.sh UGC08733 _12CO_rebase5_smooth1.3_hanning2.fits 2328.7
