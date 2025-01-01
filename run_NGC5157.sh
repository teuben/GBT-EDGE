# Created by mk_runs.py
# NGC5157 [43, 43, 60, 60] vlsr=7303.6
set -x
rm -rf NGC5157
./reduce.py   -g 43 -f 2,12 NGC5157
./reduce.py   -g 60 NGC5157
./plots.sh NGC5157 _12CO_rebase5_smooth1.3_hanning2.fits 7303.6
