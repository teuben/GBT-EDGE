# Created by mk_runs.py
# NGC5954 [20, 20] vlsr=1922.1
set -x
rm -rf NGC5954
./reduce.py -m mask_NGC5954_Havfield_v1.fits -g 20 NGC5954
./plots.sh NGC5954 _12CO_rebase5_smooth1.3_hanning2.fits 1922.1
