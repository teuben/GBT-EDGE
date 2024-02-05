# Created by mk_runs.py
# IC3598 [17, 17, 33, 33] vlsr=7635.6
set -x
rm -rf IC3598
./reduce.py -g -m mask_IC3598_Havfield_v1.fits 17 IC3598
./reduce.py -g -m mask_IC3598_Havfield_v1.fits 33 -f 2 IC3598
./plots.sh IC3598 _12CO_rebase5_smooth1.3_hanning2.fits 7635.6
