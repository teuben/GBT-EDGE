# Created by mk_runs.py
# NGC5216 [25, 25, 25] vlsr=2920.5
set -x
rm -rf NGC5216
./reduce.py -g -m mask_NGC5216_Havfield_v1.fits 25 NGC5216
./plots.sh NGC5216 _12CO_rebase5_smooth1.3_hanning2.fits 2920.5
