# Created by mk_runs.py
# UGC04245 [8, 8, 32, 32, 35, 35, 37, 37] vlsr=5169.3
set -x
rm -rf UGC04245
./reduce.py -g -m mask_UGC04245_Havfield_v1.fits 8 UGC04245
./reduce.py -g -m mask_UGC04245_Havfield_v1.fits 32,35,37 -f 2 UGC04245
./plots.sh UGC04245 _12CO_rebase5_smooth1.3_hanning2.fits 5169.3
