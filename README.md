PyPWA [![Build Status](https://travis-ci.org/JeffersonLab/PyPWA.svg?branch=development)](https://travis-ci.org/JeffersonLab/PyPWA) [![Coverage Status](https://coveralls.io/repos/github/JeffersonLab/PyPWA/badge.svg?branch=development)](https://coveralls.io/github/JeffersonLab/PyPWA?branch=development)
=====

A python based software framework designed to perform Partial Wave and 
Amplitude Analysis with the goal of extracting resonance information from 
multi-particle final states.
Is constantly tested to work with Python Version 3.7

<!--Has support for multiple likelihoods, including:
 - Extended Log Likelihood
 - Standard Log Likelihood, Optionally Binned
 - Binned ChiSquared Likelihood
 - Standard ChiSquared Likelihood
 
 You can even define your own likelihood, or calculate entirely without one
 if you chose to do so!
 -->
 
Currently being updated to PyPWA 3 (Summer 2019)
------------------------------------------------

There is an ongoing project for PyPWA to integrate various complex models
directly into PyPWA as well as decoupling interface logic from program
logic so that we may add a fully functioning GUI to the package.

Progress:
- Analysis programs:
  - [X] pysimulate
  - [ ] pyfit
    - [ ] New interface needs to be written
    - [ ] Model selection metadata needs to be finalized
  - [ ] pyproject (replaces pythonPWA)
    - [ ] Allow for work on large projects involving bins of data
    - [ ] Handle multiple subprojects for different data and fit types
    - [ ] Visualization for fits and data
- Data Programs
  - [ ] PyMask
    - [ ] Renamed to pydata
    - [X] Able to both mask data and convert data between simple types
  - [ ] pyhd5 (Pending title, partially in place)
    - [ ] Rename to pyhd5 from pydata
    - [X] Load data into hdf5 tables
    - [X] Support multivariable binning inside the table
    - [X] Optionally write data back from table
 
 
Features
--------

Generic Fitting Tools
<!--
- PyFit
  - Can fit to a log-likelihood, chi-square, or you can define your own
  - Supports Binned Data
  - Supports a quality factor per event -->
- PySimulate
- Easy to use Yaml based configuration
- A configuration builder, to walk you through the initial creation of 
  the configuration
- Supports using all the threads on the machine


Using from GitHub
-----------------

Clone the master branch onto your computer, or if you are daring clone the 
development branch

     $ git clone https://github.com/JeffersonLab/PyPWA

Setup and activate a virtualenv:

     $ virtualenv --system-site-packages venv
     $ source venv/bin/activate

Install the package inside the virtualenv:

     $ pip install .


Contribute or Support
---------------------
If you have any issues, or would like to see any features added to the 
project, let us know!

- Issue and Feature Tracker: <https://www.github.com/JeffersonLab/PyPWA/issues>
- Source Code: <https://www.github.com/JeffersonLab/PyPWA>


License
-------

The project is licensed under the GPLv3 license.

