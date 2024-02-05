# Created by mk_runs.py
# UGC04659 [3, 3] vlsr=1720.2
set -x
rm -rf UGC04659
./reduce.py -g -m mask_UGC04659_Havfield_v1.fits 3 UGC04659
./plots.sh UGC04659 _12CO_rebase5_smooth1.3_hanning2.fits 1720.2
