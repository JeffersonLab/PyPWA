PyPWA [![Build Status](https://travis-ci.org/JeffersonLab/PyPWA.svg?branch=master)](https://travis-ci.org/JeffersonLab/PyPWA)
=====

A python based software framework designed to perform Partial Wave and Amplitude Analysis with the goal of extracting resonance information from multi-particle final states.
Supports the Un/Extended Un/Binned likelihood maximum estimation, Acceptance Rejection Method, and ISOBAR Model.
Is constantly tested to work with Python Versions 2.7, 3.4, 3.5, and 3.6.

Features
--------

Generic Fitting Tools
- PyFit
 - Can fit to a log-likelihood, chi-square, or you can define your own
 - Supports Binned Data
 - Supports a quality factor per event
- PySimulate
- Easy to use Yaml based configuration
- A configuration builder, to walk you through the initial creation of the configuration
- Supports using all the CPUs on the machine

More Documentation
------------------

For in-depth details on:
- Installation
- Usage
- Examples of how to use
- How to help

Visit our online documentation at: https://pypwa.readthedocs.io

Installation
------------

Clone the master branch onto your computer, or if you are daring clone the development branch

     $ git clone https://github.com/JeffersonLab/PyPWA

Then install the package to your system, run this from inside the PyPWA folder:

     $ sudo python setup.py install


Using PyFit and PySimulate
--------------------------

Go to the directory that you would like to do your analysis in and run:

     $ Py[Fit/Simulate] -wc [configuration_name]

Fill in the data in that configuration file using your favorite editor,
then run your analysis:

     $ Py[Fit/Simulate] [configuration_name]


Contribute
----------

- Issue Tracker: <https://www.github.com/JeffersonLab/PyPWA/issues>
- Source Code: <https://www.github.com/JeffersonLab/PyPWA>

Support
-------

If you have any issues, or would like to see any features added to the project, let us know!

- Mail list: pypwa@jlab.org

License
-------

The project is licensed under the GPLv3 license.