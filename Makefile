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

# git directories we should have here

GIT_DIRS = gbtpipe degas maskmoment

# URLs that we'll need

URL1  = https://github.com/GBTSpectroscopy/gbtpipe
URL2  = https://github.com/GBTSpectroscopy/degas
URL3  = https://github.com/astroumd/lmtoy
URL4  = https://github.com/teuben/maskmoment


.PHONY:  help install build


help install:
	@echo "The installation has a few manual steps:"
	@echo ""

git:  $(GIT_DIRS)
	@echo Last git: `date` >> git.log

pull:
	@echo -n "lmtoy: "; git pull
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git pull); done
	@echo Last pull: `date` >> git.log

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
	git clone $(URL4)

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

#  running at GBO, rawdata just points to /home/sdfits
#  offsite you will need to supply your own, YMMV

rawdata:
	@if [ -d $(SDIR) ]; then \
	  ln -s $(SDIR) rawdata; \
	else \
	  echo "Not at GBO; Provide your own symlink/directory named 'rawdata'"; \
          echo "or get a precomputed dataset via: make NGC0001"; \
	  echo "SDIR=$(SDIR)"; \
	fi

weather:
	@if [ -d $(WDIR) ]; then \
	  ln -s $(WDIR) weatherd; \
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

bench0:
	$(OMP) $(TIME) ./reduce.py NGC0001

#  all procs:    556.80user   7.36system  3:17.45elapsed 285%CPU    (peter's laptop - i5-1135G7)
#  1 processor   182.82user   3.72system  3:06.68elapsed  99%CPU    (peter's laptop)
#  all procs:   3068.26user 178.50system 10:22.19elapsed 521%CPU    (at GBO's fourier machine - Xeon E5620)
#  1 processor   536.42user  10.68system 10:25.20elapsed  87%CPU    (at GBO's fourier machine)
bench1:	NGC0001
	$(OMP) $(TIME) ./reduce.py -s NGC0001

NGC0001:
	wget -q https://www.astro.umd.edu/~teuben/edge/data/NGC0001.tar -O - | tar xvf -

other:
	pip install pyspeckit

#  rsync:   only useful if you are at GBO and want to rsync to your offline location
#  if you want to fully reduce the data off-line
SEQ = 01
REM = teuben@lma.astro.umd.edu:/lma1/teuben/
rsync:
	@echo rsync to REM=$(REM) and SEQ=$(SEQ)
	du -sh $(SDIR)/AGBT21B_024_$(SEQ)
	@echo rawdata SEQ=$(SEQ)
	-rsync -ahv --bwlimit=8000 $(SDIR)/AGBT21B_024_$(SEQ) $(REM)/GBTRawdata
	@echo weather
	-rsync -ahv --bwlimit=8000 $(WDIR)/Coeffs* $(REM)/GBTWeather

#  produce a sample edge.sh
edge.sh:
	@echo '#  this is a sample edge.sh file, edit as need be'
	@echo "export GBTWEATHER=$(PWD)/weather/"
	@echo "source $(PWD)/lmtoy/python_start.sh"
	@echo "# for a virtual environment, un-comment this:"
	@echo "# source $(PWD)/edge_env/bin/activate"

#
show:
	@grep -v ^# gals.pars | awk '{if (NF>0) print $$1}' | sort  | uniq
