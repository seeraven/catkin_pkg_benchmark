catkin_pkg_benchmark
====================

[![Build Status](https://travis-ci.com/seeraven/catkin_pkg_benchmark.svg?branch=master)](https://travis-ci.com/seeraven/catkin_pkg_benchmark)

A comparison about the default `catkin_pkg` found at
https://github.com/ros-infrastructure/catkin_pkg and a speedup implemented in
https://github.com/seeraven/catkin_pkg (branch `topological_order_speedup`).


Executing the Benchmark
-----------------------

Clone this repository and call

    make bench.venv


Development
-----------

All available tests are instrumented in the `Makefile`. To get a list of all
available targets call

    make help

All main targets can be executed in a venv environment by using the `.venv`
suffix. For example, all style checks are executed in a venv environment by
calling

    make check-style.venv

