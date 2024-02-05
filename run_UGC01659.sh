# Created by mk_runs.py
# UGC01659 [1, 1] vlsr=8195.4
set -x
rm -rf UGC01659
./reduce.py -g -m mask_UGC01659_Havfield_v1.fits 1 UGC01659
./plots.sh UGC01659 _12CO_rebase5_smooth1.3_hanning2.fits 8195.4
