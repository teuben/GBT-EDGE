# Created by mk_runs.py
# NGC3106 [7, 7] vlsr=6198.4
set -x
rm -rf NGC3106
./reduce.py -m mask_NGC3106_Havfield_v1.fits -g 7 NGC3106
./plots.sh NGC3106 _12CO_rebase5_smooth1.3_hanning2.fits 6198.4
