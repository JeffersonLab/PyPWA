# PyPWA [![Build Status](https://travis-ci.org/JeffersonLab/PyPWA.svg?branch=master)](https://travis-ci.org/JeffersonLab/PyPWA)
A python based software framework designed to perform Partial Wave and Amplitude Analysis with the goal of extracting resonance information from multiparticle final states. Supports the Un/Extended Un/Binned likelihood maximum estimation, Acceptance Rejection Method, and ISOBAR Model.


## Current Status
Currently we are attempting to port all previously written tools into a object oriented package that can be easily installed and used on any posix system.
- [X] General Fitting Port
- [X] General Simulator Port
- [X] Multiprocessing implemented
- [X] Tests implemented
- [X] Automated Documentation
- [ ] Xeon Phi support offloading
- [ ] Gamp Masker Implemented
- [ ] ISOBAR Port
- [ ] PBS Support
- [ ] Tkinter replaced by PyQt4
- [ ] Support Gamp Data

## General Shell

The new General Shell is iminuit based threaded fitting tool, it is designed to run from your machines path or from a virtualenv.

To install simply run "python setup.py install", or optionally "python setup.py install --user" to install it locally instead of to your system

To use, run "GeneralFitting -wc" to have the GeneralShell write an Example.py and Example.yml to your current working directory.
After modifying the Examples to fit your use case, run "GeneralFitting -c <your config file>.yml"

