# Created by mk_runs.py
# NGC2596 [22, 22, 32, 32, 35, 35, 37, 37, 40, 40, 40] vlsr=5925.7
set -x
rm -rf NGC2596
./reduce.py -m mask_NGC2596_Havfield_v1.fits -g 22 NGC2596
./reduce.py -m mask_NGC2596_Havfield_v1.fits -g 32,40 -f 2 NGC2596
./reduce.py -m mask_NGC2596_Havfield_v1.fits -g 35,37 -f 2,6 NGC2596
./plots.sh NGC2596 _12CO_rebase5_smooth1.3_hanning2.fits 5925.7
