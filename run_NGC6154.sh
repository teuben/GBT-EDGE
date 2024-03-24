# Created by mk_runs.py
# NGC6154 [51, 51, 51, 51] vlsr=5978.5
set -x
rm -rf NGC6154
./reduce.py   -g 51 -f 2 NGC6154
./plots.sh NGC6154 _12CO_rebase5_smooth1.3_hanning2.fits 5978.5
