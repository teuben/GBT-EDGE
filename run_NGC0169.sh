# Created by mk_runs.py
# NGC0169 [2, 2, 30, 30, 36] vlsr=4598.2
set -x
rm -rf NGC0169
./reduce.py -m mask_NGC0169_Havfield_v1.fits -g 2 NGC0169
./reduce.py -m mask_NGC0169_Havfield_v1.fits -g 36 -f 2 NGC0169
./plots.sh NGC0169 _12CO_rebase5_smooth1.3_hanning2.fits 4598.2
