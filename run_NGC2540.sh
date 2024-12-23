# Created by mk_runs.py
# NGC2540 [7, 7, 48, 48, 59, 59] vlsr=6243.0
set -x
rm -rf NGC2540
./reduce.py -m mask_NGC2540_Havfield_v1.fits -g 7,59 NGC2540
./reduce.py -m mask_NGC2540_Havfield_v1.fits -g 48 -f 2 NGC2540
./plots.sh NGC2540 _12CO_rebase5_smooth1.3_hanning2.fits 6243.0
