# Created by mk_runs.py
# NGC2449 [2, 2, 33, 33] vlsr=4874.6
set -x
rm -rf NGC2449
./reduce.py -g -m mask_NGC2449_Havfield_v1.fits 2 NGC2449
./reduce.py -g -m mask_NGC2449_Havfield_v1.fits 33 -f 2 NGC2449
./plots.sh NGC2449 _12CO_rebase5_smooth1.3_hanning2.fits 4874.6
