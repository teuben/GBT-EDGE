# Created by mk_runs.py
# NGC5888 [20, 20, 21, 21] vlsr=8727.6
set -x
rm -rf NGC5888
./reduce.py -m mask_NGC5888_Havfield_v1.fits -g 20,21 NGC5888
./plots.sh NGC5888 _12CO_rebase5_smooth1.3_hanning2.fits 8727.6
