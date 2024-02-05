# Created by mk_runs.py
# NGC0932 [2, 2, 26, 26] vlsr=4072.8
set -x
rm -rf NGC0932
./reduce.py -g -m mask_NGC0932_Havfield_v1.fits 2 NGC0932
./plots.sh NGC0932 _12CO_rebase5_smooth1.3_hanning2.fits 4072.8
