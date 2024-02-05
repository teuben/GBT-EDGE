# Created by mk_runs.py
# NGC3057 [8, 8] vlsr=1482.1
set -x
rm -rf NGC3057
./reduce.py -m mask_NGC3057_Havfield_v1.fits -g 8 NGC3057
./plots.sh NGC3057 _12CO_rebase5_smooth1.3_hanning2.fits 1482.1
