# Created by mk_runs.py
# NGC3406NED01 [44, 44] vlsr=7411.6
set -x
rm -rf NGC3406NED01
./reduce.py -g   44 -f 2 NGC3406NED01
./plots.sh NGC3406NED01 _12CO_rebase5_smooth1.3_hanning2.fits 7411.6
