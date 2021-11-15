# GBT-EDGE

This toolkit helps you reducing the GBT EDGE data.
Still very preliminary, expect updates, here
as well as in 3rd party code mentioned here.

Example of use (in this directory):

      cd /home/astro-util/projects/gbt-edge/GBT-EDGE-pipeline        # at GBO
      source edge.sh
      ./reduce.py NGC0001
	  ./mmaps.py NGC0001
	  
each galaxy takes about 20 mins to reduce, where the observing time was about 60 mins.
The use of the **edge.sh** script is optional in your installation, as long as the needed packages are
installed in *your* python (see Installation below). However, at GBO it is required.

You can push your luck by trying the example maskmoment based **mmaps.py** script which tries a number
of methods to make moment maps.

# Installation

      git clone https://github.com/teuben/GBT-EDGE

There are short-cuts in the Makefile, but basically you need to 
install the following python packages in your python3 environment:

* **gbtpipe**: https://github.com/GBTSpectroscopy/gbtpipe
* **degas**:   https://github.com/GBTSpectroscopy/degas

Probably better to use the source based "install -e", so you can "git pull" while code updates are being made:

      make git
      (cd gbtpipe; pip install -e .)
      (cd degas;   pip install -e .)
      pip install pyspeckit
	  
It was noted that python > 3.7 was needed, where GBO runs 3.6.8. I've use the lmtoy method to
install a container with anaconda3's python. Also the installation of gbtpipe might need the
bz2 library. On my ubuntu system I needed to install **libbz2-dev** for this to pass the cfitsio
installation that was needed for **gbtpipe**

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

# Caveats

1. Although the **-s** can be handy, re-running the **reduce.py** script can be dangerous, as any 
   corrupt files that are in the galaxy working directory, will we wildcarded and taking into the gridding
   step.   In case of doubt, remove the directory before starting a fresh new run.   This also implies you 
   cannot make a differ RA and DEC map without removing all files and perhaps renaming. If you want to make
   separate RA and DEC maps, the gals.pars file will need to have commented out the other map, and the
   
	     edit gals.pars
		 rm -rf NGC0001
         ./reduce.py NGC0001 ;  mv NGC0001 NGC0001_RA
	     edit gals.pars
         ./reduce.py NGC0001 ;  mv NGC0001 NGC0001_DEC
		 
2. Because of the randomized sampler in the PCA methods (i.e., the svd_solver option
   here https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) the results are not reproducable
   on a few mK level.  The solver is high efficiency but can lead to different outcomes.

3. A few notes on CPU times: the **-s"" flags makes the code run about 2x faster, but always inspect if the galaxy directory
   has the feed files that you expect! Using the weather information make the code
   run maybe 5% slower, not a huge effect. On fourier NGC0001 took about 10 mins, on my i5-1135G7 laptop 4 mins.



# Important Files and Directories

* GBTEDGE.cat - this should also be in  /home/astro-util/projects/gbt-edge/GBTEDGE.cat 
* night1.py - a bruteforce example script for Night 1 (Nov 5/6, 2021)
* reduce.py - reduce one (or more) galaxies, based on parameters in gals.pars
* gals.pars - galaxy parameter file for reduce.py containing the seq/scans 
* rawdata/ - symlink to where the rawdata are stored
* weather/ - symlink to where the GBT Weather data are stored (with Coeff*.txt files)
* /home/sdfits/AGBT21B_024_01/ - night1 VEGAS raw data directory @ GBO  (1.3GB)
