# Created by mk_runs.py
# NGC0776 [4, 4, 27, 28, 28, 30, 31, 31, 37, 37, 40, 40, 40, 40] vlsr=4866.2
set -x
rm -rf NGC0776
./reduce.py -m mask_NGC0776_Havfield_v1.fits -g 4 NGC0776
./reduce.py -m mask_NGC0776_Havfield_v1.fits -g 37 -f 2,6 NGC0776
./reduce.py -m mask_NGC0776_Havfield_v1.fits -g 40 -f 2 NGC0776
./plots.sh NGC0776 _12CO_rebase5_smooth1.3_hanning2.fits 4866.2
