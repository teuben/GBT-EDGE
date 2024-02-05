# Created by mk_runs.py
# UGC09777 [15, 18] vlsr=4663.4
set -x
rm -rf UGC09777
./reduce.py -g -m mask_UGC09777_Havfield_v1.fits 15,18 UGC09777
./plots.sh UGC09777 _12CO_rebase5_smooth1.3_hanning2.fits 4663.4
