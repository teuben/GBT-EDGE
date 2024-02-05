# Created by mk_runs.py
# UGC09629 [13, 13, 42, 42, 42, 42] vlsr=7794.9
set -x
rm -rf UGC09629
./reduce.py -m mask_UGC09629_Havfield_v1.fits -g 13 UGC09629
./reduce.py -m mask_UGC09629_Havfield_v1.fits -g 42 -f 2 UGC09629
./plots.sh UGC09629 _12CO_rebase5_smooth1.3_hanning2.fits 7794.9
