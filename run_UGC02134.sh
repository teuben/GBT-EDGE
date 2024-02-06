# Created by mk_runs.py
# UGC02134 [4, 4, 26, 26, 28, 28, 29, 34, 34] vlsr=4540.0
set -x
rm -rf UGC02134
./reduce.py -m mask_UGC02134_Havfield_v1.fits -g 4 UGC02134
./reduce.py -m mask_UGC02134_Havfield_v1.fits -g 34 -f 2 UGC02134
./plots.sh UGC02134 _12CO_rebase5_smooth1.3_hanning2.fits 4540.0
