# See the INSTALL.md notes on how to use this Makefile
# what is shown here to install, is just one of many paths

#
SHELL = /bin/bash

# use standard wget or Peter's caching wgetc 
WGET = wget

# use python3 or anaconda3
PYTHON = anaconda3

# git directories we should have here

GIT_DIRS = gbtpipe degas

# URLs that we'll need

URL1  = https://github.com/GBTSpectroscopy/gbtpipe
URL2  = https://github.com/GBTSpectroscopy/degas

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


edge_env:
	python3 -m venv edge_env

install_gbtpipe:  gbtpipe edge_env
	(cd gbtpipe;\
	cd ../edge_env/bin/activate;\
	pip3 install --upgrade pip;\
	pip3 install -e .)

install_degas:  degas edge_env
	(cd degas;\
	cd ../edge_env/bin/activate;\
	pip3 install --upgrade pip;\
	pip3 install -e .)
