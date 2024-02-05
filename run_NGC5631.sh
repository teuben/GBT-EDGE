# Created by mk_runs.py
# NGC5631 [18, 18] vlsr=1939.3
set -x
rm -rf NGC5631
./reduce.py -g -m mask_NGC5631_Havfield_v1.fits 18 NGC5631
./plots.sh NGC5631 _12CO_rebase5_smooth1.3_hanning2.fits 1939.3
