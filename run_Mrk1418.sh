# Created by mk_runs.py
# Mrk1418 [41, 41] vlsr=759.0
set -x
rm -rf Mrk1418
./reduce.py -m mask_Mrk1418_rotcur.fits -g 41 -f 2 Mrk1418
./plots.sh Mrk1418 _12CO_rebase5_smooth1.3_hanning2.fits 759.0
