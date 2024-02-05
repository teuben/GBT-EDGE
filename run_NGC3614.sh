# Created by mk_runs.py
# NGC3614 [14, 14] vlsr=2305.6
set -x
rm -rf NGC3614
./reduce.py -g -m mask_NGC3614_Havfield_v1.fits 14 NGC3614
./plots.sh NGC3614 _12CO_rebase5_smooth1.3_hanning2.fits 2305.6
