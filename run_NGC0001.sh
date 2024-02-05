# Created by mk_runs.py
# NGC0001 [1, 1, 26, 26, 27, 29, 29, 31, 36, 38, 38, 38, 38] vlsr=4485.7
set -x
rm -rf NGC0001
./reduce.py -g -m mask_NGC0001_Havfield_v1.fits 1 NGC0001
./reduce.py -g -m mask_NGC0001_Havfield_v1.fits 36,38 -f 2 NGC0001
./plots.sh NGC0001 _12CO_rebase5_smooth1.3_hanning2.fits 4485.7
