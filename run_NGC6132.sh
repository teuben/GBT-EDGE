# Created by mk_runs.py
# NGC6132 [18, 18, 49, 49] vlsr=4986.6
set -x
rm -rf NGC6132
./reduce.py -m mask_NGC6132_Havfield_v1.fits -g 18 NGC6132
./reduce.py -m mask_NGC6132_Havfield_v1.fits -g 49 -f 2 NGC6132
./plots.sh NGC6132 _12CO_rebase5_smooth1.3_hanning2.fits 4986.6
