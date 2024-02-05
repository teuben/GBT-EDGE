# Created by mk_runs.py
# NGC3353 [42, 42] vlsr=976.2
set -x
rm -rf NGC3353
./reduce.py   -g 42 -f 2 NGC3353
./plots.sh NGC3353 _12CO_rebase5_smooth1.3_hanning2.fits 976.2
