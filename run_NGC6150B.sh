# Created by mk_runs.py
# NGC6150B [51, 51] vlsr=9494.1
set -x
rm -rf NGC6150B
./reduce.py   -g 51 -f 2 NGC6150B
./plots.sh NGC6150B _12CO_rebase5_smooth1.3_hanning2.fits 9494.1
