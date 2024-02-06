# Created by mk_runs.py
# NGC0495 [6, 6] vlsr=4045.8
set -x
rm -rf NGC0495
./reduce.py -m mask_NGC0495_Havfield_v1.fits -g 6 NGC0495
./plots.sh NGC0495 _12CO_rebase5_smooth1.3_hanning2.fits 4045.8
