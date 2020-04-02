# ----------------------------------------------------------------------------
# Makefile for catkin_pkg_benchmark
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of catkin_pkg_benchmark and is
# released under the "BSD 3-Clause License". Please see the LICENSE file that
# is included as part of this package.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#  SETTINGS
# ----------------------------------------------------------------------------

DIR_VENV  = venv
SHELL     = /bin/bash


# ----------------------------------------------------------------------------
#  DEFAULT TARGETS
# ----------------------------------------------------------------------------

.PHONY: help system-setup venv-bash check-style-venv pylint pycodestyle flake8 test clean

all:	check-style.venv bench.venv


# ----------------------------------------------------------------------------
#  USAGE
# ----------------------------------------------------------------------------
help:
	@echo "Makefile for catkin_pkg_benchmark"
	@echo "================================="
	@echo
	@echo "Targets for Style Checking in venv:"
	@echo " check-style.venv   : Call pylint, pycodestyle and flake8"
	@echo " pylint.venv        : Call pylint on the source files."
	@echo " pycodestyle.venv   : Call pycodestyle on the source files."
	@echo " flake8.venv        : Call flake8 on the source files."
	@echo
	@echo "Targets for Style Checking in System Environment:"
	@echo " check-style        : Call pylint, pycodestyle and flake8"
	@echo " pylint             : Call pylint on the source files."
	@echo " pycodestyle        : Call pycodestyle on the source files."
	@echo " flake8             : Call flake8 on the source files."
	@echo
	@echo "Targets for Benchmark in venv:"
	@echo " bench.venv         : Execute the benchmark."
	@echo
	@echo "Targets for Benchmark in System Environment:"
	@echo " bench              : Execute the benchmark."
	@echo
	@echo "venv Setup:"
	@echo " venv               : Create the venv."
	@echo " venv-bash          : Start a new shell in the venv for debugging."
	@echo
	@echo "Misc Targets:"
	@echo " catkin_pkg_orig    : Clone the original catkin_pkg."
	@echo " catkin_pkg_speedup : Clone the catkin_pkg with speedup branch."
	@echo " system-setup       : Install all dependencies in the currently"
	@echo "                      active environment (system or venv)."
	@echo " clean              : Remove all temporary files."
	@echo


# ----------------------------------------------------------------------------
#  SYSTEM SETUP
# ----------------------------------------------------------------------------

catkin_pkg_orig:
	@git clone https://github.com/seeraven/catkin_pkg catkin_pkg_orig

catkin_pkg_speedup:
	@git clone https://github.com/seeraven/catkin_pkg catkin_pkg_speedup
	@cd catkin_pkg_speedup && git checkout topological_order_speedup

system-setup:
	@echo "-------------------------------------------------------------"
	@echo "Installing pip..."
	@echo "-------------------------------------------------------------"
	@pip install -U pip
	@echo "-------------------------------------------------------------"
	@echo "Installing package requirements..."
	@echo "-------------------------------------------------------------"
	@pip install -r requirements.txt
	@echo "-------------------------------------------------------------"
	@echo "Installing package development requirements..."
	@echo "-------------------------------------------------------------"
	@pip install -r dev_requirements.txt


# ----------------------------------------------------------------------------
#  VENV SUPPORT
# ----------------------------------------------------------------------------

venv:
	@if [ ! -d $(DIR_VENV) ]; then python3 -m venv $(DIR_VENV); fi
	@source $(DIR_VENV)/bin/activate; \
	make system-setup
	@echo "-------------------------------------------------------------"
	@echo "Virtualenv $(DIR_VENV) setup. Call"
	@echo "  source $(DIR_VENV)/bin/activate"
	@echo "to activate it."
	@echo "-------------------------------------------------------------"


venv-bash: venv
	@echo "Entering a new shell using the venv setup:"
	@source $(DIR_VENV)/bin/activate; \
	/bin/bash
	@echo "Leaving sandbox shell."


%.venv: venv
	@source $(DIR_VENV)/bin/activate; \
	make $*


# ----------------------------------------------------------------------------
#  STYLE CHECKING
# ----------------------------------------------------------------------------

check-style: pylint pycodestyle flake8

pylint:
	@pylint --rcfile=.pylintrc tools/*.py
	@echo "pylint found no errors."


pycodestyle:
	@pycodestyle --config=.pycodestyle tools/*.py
	@echo "pycodestyle found no errors."


flake8:
	@flake8 tools/*.py
	@echo "flake8 found no errors."


# ----------------------------------------------------------------------------
#  BENCHMARK
# ----------------------------------------------------------------------------

bench: catkin_pkg_orig catkin_pkg_speedup
	@echo
	@echo "Original catkin_pkg:"
	@PYTHONPATH=catkin_pkg_orig/src tools/test_topological_order.py src
	@echo "--------------------------------------------------------------"
	@echo
	@echo "Modified catkin_pkg:"
	@PYTHONPATH=catkin_pkg_speedup/src tools/test_topological_order.py src
	@echo "--------------------------------------------------------------"


# ----------------------------------------------------------------------------
#  MAINTENANCE TARGETS
# ----------------------------------------------------------------------------

clean:
	@find . -iname "*~" -exec rm -f {} \;
	@find . -iname "*.pyc" -exec rm -f {} \;
	@rm -rf venv catkin_pkg_orig catkin_pkg_speedup

