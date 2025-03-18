# Created by mk_runs.py
# NGC0932 [2, 2, 26, 26, 55, 55, 57, 57, 57, 57] vlsr=4072.8
set -x
rm -rf NGC0932
./reduce.py -m mask_NGC0932_Havfield_v1.fits -g 2,55,57 NGC0932
./plots.sh NGC0932 _12CO_rebase5_smooth1.3_hanning2.fits 4072.8
