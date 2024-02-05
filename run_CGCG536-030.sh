# Created by mk_runs.py
# CGCG536-030 [6, 10] vlsr=5973.5
set -x
rm -rf CGCG536-030
./reduce.py -m mask_CGCG536-030_Havfield_v1.fits -g 6,10 CGCG536-030
./plots.sh CGCG536-030 _12CO_rebase5_smooth1.3_hanning2.fits 5973.5
