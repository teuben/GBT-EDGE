# Created by mk_runs.py
# NGC5402 [45, 45, 50, 50] vlsr=3011.7
set -x
rm -rf NGC5402
./reduce.py   -g 45,50 -f 2 NGC5402
./plots.sh NGC5402 _12CO_rebase5_smooth1.3_hanning2.fits 3011.7
