# Created by mk_runs.py
# NGC4003 [8, 14, 32, 32, 46, 46] vlsr=6546.2
set -x
rm -rf NGC4003
./reduce.py -m mask_NGC4003_Havfield_v1.fits -g 8,14 NGC4003
./reduce.py -m mask_NGC4003_Havfield_v1.fits -g 32,46 -f 2 NGC4003
./plots.sh NGC4003 _12CO_rebase5_smooth1.3_hanning2.fits 6546.2
