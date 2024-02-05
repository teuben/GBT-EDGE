# Created by mk_runs.py
# UGC03960 [41, 41] vlsr=2222.5
set -x
rm -rf UGC03960
./reduce.py -g -m mask_UGC03960_Havfield_v1.fits 41 -f 2 UGC03960
./plots.sh UGC03960 _12CO_rebase5_smooth1.3_hanning2.fits 2222.5
