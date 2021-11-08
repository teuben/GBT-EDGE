# GBT-EDGE

example scripts to reduce GBT EDGE data. Still very preliminary, expect updates, here
as well as in 3rd party code mentioned here.

# Installation

There are short-cuts in the Makefile, but basically you need to 
install the following python packages in your whatever python3 environment you use:

* gbtpipe: https://github.com/GBTSpectroscopy/gbtpipe
* degas:   https://github.com/GBTSpectroscopy/degas

Probably better to use the source based install, so you can "git pull" while code updates are being made:

	  cd gbtpipe
      pip install -e .
	  
It was noted that python > 3.7 was needed, where GBO runs 3.6.8. I've use the lmtoy method to
install a container with anaconda3's python.
	  
	  
# Running

Since the weather info is nominally only available at GBO, you should run this on a GBO machine.
For those wishing to run this locally, consult the degas instructions
[here](https://github.com/GBTSpectroscopy/degas/blob/master/README.md#local-installation-of-the-degas-pipeline).

# Important Files and Directories

* GBTEDGE.cat - this should also be in  /home/astro-util/projects/gbt-edge/GBTEDGE.cat 
* night1.py - a bruteforce example script for Night 1 (Nov 5/6, 2021)
* /home/sdfits/AGBT21B_024_01 - night1 VEGAS raw data @ GBO  (1.3GB)
