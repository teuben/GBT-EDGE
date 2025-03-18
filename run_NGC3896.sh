# Created by mk_runs.py
# NGC3896 [42, 42, 60, 60] vlsr=880.3
set -x
rm -rf NGC3896
./reduce.py   -g 42 -f 2 NGC3896
./reduce.py   -g 60 NGC3896
./plots.sh NGC3896 _12CO_rebase5_smooth1.3_hanning2.fits 880.3
