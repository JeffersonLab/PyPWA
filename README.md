PyPWA
=====

JLab PWA software infrastructure

A software framework used to perform Partial Wave and Amplitude Analysis (PWA) with the goal of extracting resonance information from multiparticle final states


Current Status
------

Currently the PyPWA package is being restructured into a proper python package complete with setup tools.
As of right now only the GeneralShell has been adapted to the packaging utility, and all other tools live in limbo and are usable as before. Everything in limbo is untouched.

General Shell
------

The new General Shell is iminuit based threaded fitting tool, it is designed to run from your machines path or from a virtualenv.

To install simply run "python setup.py install", or optionally "python setup.py install --user" to install it locally instead of to your system

To use, run "GeneralFitting -wc" to have the GeneralShell write an Example.py and Example.yml to your current working directory.
After modifying the Examples to fit your use case, run "GeneralFitting -c <your config file>.yml"

