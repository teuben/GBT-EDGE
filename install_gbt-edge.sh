#! /bin/bash
#
#   this is an example install script, it likely will need to be adapted for you
#   there are no package requirements outside of python listed here.
#

echo "install_gbt-edge.sh:  4-sep-2025"

branch=main
python=1
url=https://github.com/teuben/GBT-EDGE

help() {
    echo This is a simple install script for GBT-EDGE
    echo Optional parameters are key=val, defaults are:
    echo
    echo branch=$branch
    echo python=$python
    echo url=$url
}


# indirect git clone via nemo.git for faster testing
# bootstrap with:    git clone https://github.com/teuben/nemo nemo.git
if [ -d GBT-EDGE ]; then
  echo Cannot re-install
  exit 0
fi

for arg in $*; do\
  if test $arg == --help || test $arg == -h; then
    help
    exit 0
  fi
  export $arg
done

echo "Using: "
echo "  branch=$branch"
echo "  python=$python"
echo "  url=$url"
echo ""

date0=$(date)

git clone $url
cd GBT-EDGE
git checkout $branch


#
#./install_anaconda3 wget=wgetc version=2022.10    
./install_anaconda3 wget=wgetc version=2023.03-1  

source anaconda3/python_start.sh
pip install -r requirements.txt

#   @todo   fix this
make gbtpipe degas

mv gbtpipe gbtpipe.git
mv degas   degas.git

pip install -e gbtpipe.git
pip install -e degas.git

#
pip freeze > freeze.log

ln -s ../../GBT-EDGE/masks
ln -s ../../GBT-EDGE/rawdata

export GBTWEATHER=~/EDGE/GBTWeather/


OMP_NUM_THREADS=1 /usr/bin/time ./reduce.py  -g 1 NGC0001
OMP_NUM_THREADS=1 /usr/bin/time ./reduce2.py -g 1 NGC0001


exit


#   didn't work, had to edit degas/setup.py
#echo '__version__ = "0.2"' > gbtpipe.git/gbtpipe/__version__.py
