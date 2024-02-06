# Created by mk_runs.py
# NGC5987 [21, 21] vlsr=2996.6
set -x
rm -rf NGC5987
./reduce.py -m mask_NGC5987_Havfield_v1.fits -g 21 NGC5987
./plots.sh NGC5987 _12CO_rebase5_smooth1.3_hanning2.fits 2996.6
