# Created by mk_runs.py
# NGC6497 [52, 52, 52] vlsr=6021.0
set -x
rm -rf NGC6497
./reduce.py   -g 52 -f 2 NGC6497
./plots.sh NGC6497 _12CO_rebase5_smooth1.3_hanning2.fits 6021.0
