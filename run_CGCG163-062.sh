# Created by mk_runs.py
# CGCG163-062 [15, 15] vlsr=4301.2
set -x
rm -rf CGCG163-062
./reduce.py -m mask_CGCG163-062_Havfield_v1.fits -g 15 CGCG163-062
./plots.sh CGCG163-062 _12CO_rebase5_smooth1.3_hanning2.fits 4301.2
