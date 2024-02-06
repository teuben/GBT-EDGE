# Created by mk_runs.py
# NGC5267 [19, 19] vlsr=5936.6
set -x
rm -rf NGC5267
./reduce.py -m mask_NGC5267_Havfield_v1.fits -g 19 NGC5267
./plots.sh NGC5267 _12CO_rebase5_smooth1.3_hanning2.fits 5936.6
