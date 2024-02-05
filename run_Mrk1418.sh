# Created by mk_runs.py
# Mrk1418 [41, 41] vlsr=665.3
set -x
rm -rf Mrk1418
./reduce.py -g   41 -f 2 Mrk1418
./plots.sh Mrk1418 _12CO_rebase5_smooth1.3_hanning2.fits 665.3
