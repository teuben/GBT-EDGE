# Created by mk_runs.py
# NGC3619 [15, 15] vlsr=1552.9
set -x
rm -rf NGC3619
./reduce.py -g -m mask_NGC3619_Havfield_v1.fits 15 NGC3619
./plots.sh NGC3619 _12CO_rebase5_smooth1.3_hanning2.fits 1552.9
