# Created by mk_runs.py
# NGC5720 [14, 14, 14, 14] vlsr=7751.2
set -x
rm -rf NGC5720
./reduce.py -m mask_NGC5720_Havfield_v1.fits -g 14 NGC5720
./plots.sh NGC5720 _12CO_rebase5_smooth1.3_hanning2.fits 7751.2
