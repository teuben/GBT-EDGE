# Created by mk_runs.py
# NGC2691 [5, 5, 37, 40, 40, 40, 40] vlsr=3948.8
set -x
rm -rf NGC2691
./reduce.py -g -m mask_NGC2691_Havfield_v1.fits 5 NGC2691
./reduce.py -g -m mask_NGC2691_Havfield_v1.fits 37,40 -f 2 NGC2691
./plots.sh NGC2691 _12CO_rebase5_smooth1.3_hanning2.fits 3948.8
