PyPWA [![Build Status](https://travis-ci.org/JeffersonLab/PyPWA.svg?branch=development)](https://travis-ci.org/JeffersonLab/PyPWA) [![Coverage Status](https://coveralls.io/repos/github/JeffersonLab/PyPWA/badge.svg?branch=development)](https://coveralls.io/github/JeffersonLab/PyPWA?branch=development)
=====

A python based software framework designed to perform Partial Wave and 
Amplitude Analysis with the goal of extracting resonance information from 
multi-particle final states.
Is constantly tested to work with Python Version 3.7+

Has support for multiple likelihoods, including:

 - Extended Log Likelihood
 - Standard Log Likelihood, Optionally Binned
 - Binned ChiSquared Likelihood
 - Standard ChiSquared Likelihood
 
You can even define your own likelihood, or calculate entirely without one
if you chose to do so!

 
Currently being updated to PyPWA 3 (Summer 2020)
------------------------------------------------

We're currently adding fixes and documentation as we prepare for an
official PyPWA 3 release! If you notice inconsistencies in our 
documentation, or unusual slow-downs, please let us know in the issues!
 
 
Features
--------

Generic Fitting Tools

- Fitting
  - Can fit to a log-likelihood, chi-square, or you can define your own
  - Supports Binned Data
  - Supports a quality factor per event
- Simulation using Monte Carlo Rejection
- Easy to use Yaml based configuration for command line operation
- Jupyter Integration
- Supports using all the threads on the machine

Installing into Anaconda
------------------------

We've setup an user channel on Anaconda so that you can install PyPWA
into your Anaconda installation with the following command

    $ conda install -c markjonestx pypwa


Notes for Apple Users
---------------------

With testing, we've found that PyPWA's environment in Anaconda doesn't
work well with Xterm in Mac OS X, however, Terminal found in your
Utilities folder does not seem to have the same issues.


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

