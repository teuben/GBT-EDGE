#    various target to aid in installing GBT-EDGE
#
SHELL = /bin/bash

# use standard wget or Peter's caching wgetc 
WGET = wget

# use python3 or anaconda3
PYTHON = anaconda3

# timing
TIME = /usr/bin/time

# parallel?
OMP = OMP_NUM_THREADS=1

# Greenbank locations (useful for rsync)

SDIR = /home/sdfits
WDIR = /users/rmaddale/Weather/ArchiveCoeffs

# git directories we should have here and keep updated

GIT_DIRS = gbtpipe degas maskmoment edge_pydb gbtgridder

# URLs that we'll need

URL1  = https://github.com/GBTSpectroscopy/gbtpipe
URL2  = https://github.com/GBTSpectroscopy/degas
URL3  = https://github.com/astroumd/lmtoy
URL4a = https://github.com/teuben/maskmoment
URL4  = https://github.com/tonywong94/maskmoment
URL5  = https://github.com/tonywong94/edge_pydb
URL6  = https://github.com/richteague/bettermoments
URL7  = https://github.com/GreenBankObservatory/gbtgridder
URL7a = https://github.com/teuben/gbtgridder

.PHONY:  help install build

## help:     This Help
help : Makefile
	@sed -n 's/^##//p' $<

## git:      make the needed git repos (GIT_DIRS)
git:  $(GIT_DIRS)
	@echo Last git: `date` >> git.log

## pull:     update (git pull) the used git repos
pull:
	@echo -n "lmtoy: "; git pull
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git pull); done
	@echo Last pull: `date` >> git.log

## status:   query status of the used git repos
status:
	@echo -n "lmtoy: "; git status -uno
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git status -uno); done


gbtpipe:
	git clone $(URL1)

degas:
	git clone $(URL2)

lmtoy:
	git clone $(URL3)

maskmoment:
	git clone $(URL4a)

edge_pydb:
	git clone $(URL5)

gbtgridder:
	git clone -b python3 $(URL7a)

edge_env:
	python3 -m venv edge_env

# note gbtpipe needs to be installed before degas
install_gbtpipe:  gbtpipe edge_env
	(cd gbtpipe;\
	source ../edge_env/bin/activate;\
	pip3 install --upgrade pip;\
	pip3 install -e .)

install_degas:  degas edge_env
	(cd degas;\
	source ../edge_env/bin/activate;\
	pip3 install --upgrade pip;\
	pip3 install -e .)

install_maskmoment:  maskmoment edge_env
	(cd maskmoment;\
	source ../edge_env/bin/activate;\
	pip3 install --upgrade pip;\
	pip3 install -e .)

install_edge:  edge_pydb edge_env
	(cd edge_pydb;\
	source ../edge_env/bin/activate;\
	pip3 install --upgrade pip;\
	pip3 install -e .)

#  running at GBO, rawdata just points to /home/sdfits
#  offsite you will need to supply your own, YMMV
#  usually using the rsync target here, and running it from GBO
#  this also updates the weather database

## rawdata:  symlink to the SDFITS data (SDIR=)
rawdata:
	@if [ -d $(SDIR) ]; then \
	  ln -s $(SDIR) rawdata; \
	else \
	  echo "Not at GBO; Provide your own symlink/directory named 'rawdata'"; \
          echo "or get a precomputed dataset via: make NGC0001"; \
	  echo "SDIR=$(SDIR)"; \
	fi

## weather:  symlink to the GBO weather database directory (WDIR=)
weather:
	@if [ -d $(WDIR) ]; then \
	  ln -s $(WDIR) weather; \
	else \
	  echo "Not at GBO; Provide your own symlink/directory named 'weather'"; \
	  echo "WDIR=$(WDIR)"; \
	fi

# python >= 3.7 is now required
# gbt runs 3.6.8
# hack to install a more recent python
pjt:	lmtoy
	(cd lmtoy; make install_python)
	@echo "Make sure you 'source lmtoy/python_start.sh'"

data0:
	(cd rawdata; \
	wget -q https://www.astro.umd.edu/~teuben/edge/data/AGBT21B_024_01.tar -O - | tar xvf -)

# 1 processor    280.58user 6.48system 4:47.21elapsed 99%CPU
bench0:
	$(OMP) $(TIME) ./reduce.py NGC0001
	fitsccd NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits - | ccdstat - bad=0 qac=t

#  all procs:    556.80user   7.36system  3:17.45elapsed 285%CPU    (peter's laptop - i5-1135G7)
#  1 processor   182.82user   3.72system  3:06.68elapsed  99%CPU    (peter's laptop)
#  all procs:   3068.26user 178.50system 10:22.19elapsed 521%CPU    (at GBO's fourier machine - Xeon E5620)
#  1 processor   536.42user  10.68system 10:25.20elapsed  87%CPU    (at GBO's fourier machine)
bench1:	NGC0001
	$(OMP) $(TIME) ./reduce.py -g 1 -s NGC0001
	fitsccd NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits -|ccdstat - bad=0 qac=t
	fitsccd NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits -|ccdstat - bad=0 qac=t robust=t



# 1 processor:   
bench2:
	$(OMP) $(TIME) ./reduce.py -g 1 -M NGC0001
	fitsccd NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits -|ccdstat - bad=0 qac=t
	fitsccd NGC0001/NGC0001_12CO_rebase3_smooth2_hanning2.fits -|ccdstat - bad=0 qac=t robust=t

# with the standard 'mask_NGC0001_Havfield_v1.fits'

bench3:
	$(OMP) $(TIME) ./reduce.py -g 1 -m mask_NGC0001_Havfield_v1.fits NGC0001

bench4:
	./plot_spectrum.py "00:07:15.84" "+27:42:29.7" 8.4 0 0 NGC0001/NGC0001_12CO_rebase5_smooth1.3_hanning2.fits


NGC0001:
	wget -q https://www.astro.umd.edu/~teuben/edge/data/NGC0001.tar -O - | tar xvf -

other:
	pip install pyspeckit

#  rsync:   only useful if you are at GBO and want to rsync to your offline location
#  if you want to fully reduce the data off-line
SEQ = 01
REM = teuben@lma.astro.umd.edu:/n/lma1/teuben/
## rsync:    rsync to REM=$REM and SEQ=$SEQ
rsync:
	@echo rsync to REM=$(REM) and SEQ=$(SEQ)
	du -sh $(SDIR)/AGBT21B_024_$(SEQ)
	@echo rawdata SEQ=$(SEQ)
	-rsync -ahv --bwlimit=8000 $(SDIR)/AGBT21B_024_$(SEQ) $(REM)/GBTRawdata
	@echo weather
	-rsync -ahv --bwlimit=8000 $(WDIR)/Coeffs* $(REM)/GBTWeather

#  this lenghty IDL based procedure computes the mean/rms/min/max for tsys for a given SEQ
## tsys:     make tsys and summary files for SEQ=$SEQ
tsys:
	./tsys.py AGBT21B_024_$(SEQ)
	cp pro/AGBT21B_024_$(SEQ).tsys tsyslogs
	@echo git add           tsyslogs/AGBT21B_024_$(SEQ).tsys
	@echo git commit -m new tsyslogs/AGBT21B_024_$(SEQ).tsys
	cp pro/AGBT21B_024_$(SEQ).summary summarylogs
	@echo git add           summarylogs/AGBT21B_024_$(SEQ).summary
	@echo git commit -m new summarylogs/AGBT21B_024_$(SEQ).summary

## astrid:   make astridlogs for SEQ=$SEQ
astrid:
	(cd astridlogs; getastridlog AGBT21B_024_$(SEQ))
	@echo git add           astridlogs/AGBT21B_024_$(SEQ)_log.txt
	@echo git commit -m new astridlogs/AGBT21B_024_$(SEQ)_log.txt

#  produce a sample edge.sh
edge.sh:
	@echo '#  this is a sample edge.sh file, edit as need be'
	@echo "export GBTWEATHER=$(PWD)/weather/"
	@echo "source $(PWD)/lmtoy/python_start.sh"
	@echo "source $(PWD)/lmtoy/nemo/nemo_start.sh"
	@echo "# for a virtual environment, un-comment this:"
	@echo "# source $(PWD)/edge_env/bin/activate"

#
show:
	@grep -v ^# gals.pars | awk '{if (NF>0) print $$1}' | sort  | uniq


#  galaxies with masks
MGCAL = NGC0001 NGC0169 NGC0495 NGC0776 NGC0932 NGC2691  UGC01659 UGC02134 UGC02239 UGC04245

# mask_CGCG536-030_Havfield_v1.fits

# getastridlog AGBT21B_024_10
 
## stats:    make a new stats.log
stats:
	./do_all_stats > do_all_stats.log
	cp do_all_stats.log stats.log
	@echo Results in  stats.log
	./mk_summary1.py > README.html 

## sessions: report which galaxy in which session (not yet used)
sessions:
	grep -v ^\# gals.pars | awk '{if (NF>2) print $$1,$$2}'  | sort | uniq > sessions.log

## all:      create a runs.sh file to re-run the whole pipeline, ideally with slurm or gnu parallel
all:
	./mk_runs.py
	@echo "# Created by 'make all'" > runs.sh
	ls ./run_*.sh | awk '{printf("bash %s > %s.log 2>&1\n",$$1,$$1)}' >> runs.sh
	@echo 'Now run:'
	@echo '   OMP_NUM_THREADS=1  parallel --jobs 16 < runs.sh'
	@echo "e.g. 51 galaxies on 16 processors took 40 mins"
