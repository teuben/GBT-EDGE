# Created by mk_runs.py
# NGC1056 [56, 56, 56] vlsr=1538.7
set -x
rm -rf NGC1056
./reduce.py   -g 56 NGC1056
./plots.sh NGC1056 _12CO_rebase5_smooth1.3_hanning2.fits 1538.7
