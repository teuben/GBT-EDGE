# GBT-EDGE

This toolkit helps you reducing the GBT EDGE data.
Still very preliminary, expect updates, here
as well as in 3rd party code mentioned here.

Example of use (in this directory):

      source edge.sh              # optional, just to set up your (python) environment
      ./reduce.py NGC0001 
	  
each galaxy takes about 20 mins to reduce, where the observing time was about 60 mins.
The use of the **edge.sh** script is optional, as long as the needed packages are
installed in *your* python (see Installation below).

# Installation

      git clone https://github.com/teuben/GBT-EDGE

There are short-cuts in the Makefile, but basically you need to 
install the following python packages in your whatever python3 environment you use:

* **gbtpipe**: https://github.com/GBTSpectroscopy/gbtpipe
* **degas**:   https://github.com/GBTSpectroscopy/degas

Probably better to use the source based install (-e), so you can "git pull" while code updates are being made:

      make git
      pip install -e gbtpipe
      pip install -e degas
      pip install pyspeckit
	  
It was noted that python > 3.7 was needed, where GBO runs 3.6.8. I've use the lmtoy method to
install a container with anaconda3's python. Also the installation of gbtpipe might need the
bz2 library. On my ubuntu system I needed to install **libbz2-dev** for this to pass the cfitsio
installation.

The Makefile contains a few other targets that may guide you in getting a clean install.

# Sample Data

Running the calibration off-line is not impossible, but involved, since it needs on-line weather
information. However, using
one of our datasets for [NGC0001](https://www.astro.umd.edu/~teuben/edge/data/NGC0001.tar) can be
used to play with the gridding step, viz.

     make NGC0001
      ./reduce.py -s NGC0001

and skipping the calibration.

# Working Offline

To fully work offline, you will need to create symlinks from
**rawdata** and **weather** to copies of the GBT (sdfits) rawdata and
weather information. The [degas
instructions](https://github.com/GBTSpectroscopy/degas/blob/master/README.md#local-installation-of-the-degas-pipeline)
go in more detail, our **Makefile** has some useful targets to aid in
the setup.

# Important Files and Directories

* GBTEDGE.cat - this should also be in  /home/astro-util/projects/gbt-edge/GBTEDGE.cat 
* night1.py - a bruteforce example script for Night 1 (Nov 5/6, 2021)
* reduce.py - reduce one (or more) galaxies, based on parameters in gals.pars
* gals.pars - parameter file for reduce.py
* rawdata - symlink to where the rawdata are stored
* weather - symlink to where the GBT Weather data are stored 
* /home/sdfits/AGBT21B_024_01 - night1 VEGAS raw data @ GBO  (1.3GB)
