# Created by mk_runs.py
# IC0674 [18, 18, 34, 34] vlsr=7497.7
set -x
rm -rf IC0674
./reduce.py -m mask_IC0674_Havfield_v1.fits -g 18 IC0674
./reduce.py -m mask_IC0674_Havfield_v1.fits -g 34 -f 2 IC0674
./plots.sh IC0674 _12CO_rebase5_smooth1.3_hanning2.fits 7497.7
