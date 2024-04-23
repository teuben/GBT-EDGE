# Created by mk_runs.py
# NGC6338 [52] vlsr=8170.7
set -x
rm -rf NGC6338
./reduce.py   -g 52 -f 2 NGC6338
./plots.sh NGC6338 _12CO_rebase5_smooth1.3_hanning2.fits 8170.7
