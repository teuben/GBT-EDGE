# Created by mk_runs.py
# NGC5929 [51, 51] vlsr=2513.7
set -x
rm -rf NGC5929
./reduce.py   -g 51 -f 2 NGC5929
./plots.sh NGC5929 _12CO_rebase5_smooth1.3_hanning2.fits 2513.7
