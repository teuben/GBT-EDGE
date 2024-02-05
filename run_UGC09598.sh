# Created by mk_runs.py
# UGC09598 [12, 12, 13, 43, 43] vlsr=5591.1
set -x
rm -rf UGC09598
./reduce.py -g -m mask_UGC09598_Havfield_v1.fits 12,13 UGC09598
./reduce.py -g -m mask_UGC09598_Havfield_v1.fits 43 -f 2,12 UGC09598
./plots.sh UGC09598 _12CO_rebase5_smooth1.3_hanning2.fits 5591.1
