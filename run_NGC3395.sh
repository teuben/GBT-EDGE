# Created by mk_runs.py
# NGC3395 [17, 17, 33, 33] vlsr=1575.1
set -x
rm -rf NGC3395
./reduce.py -g -m mask_NGC3395_Havfield_v1.fits 17 NGC3395
./reduce.py -g -m mask_NGC3395_Havfield_v1.fits 33 -f 2 NGC3395
./plots.sh NGC3395 _12CO_rebase5_smooth1.3_hanning2.fits 1575.1
