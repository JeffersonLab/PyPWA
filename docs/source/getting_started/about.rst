#####
About
#####

The PyPWA Project aims to develop a software framework that can be used to
perform parametric model fitting to data. In particular, Partial Wave and
Amplitude Analysis (PWA) of multiparticle final states. PyPWA is designed
for photoproduction experiments using linearly polarized photon beams. The
software makes use of the resources at the JLab Scientific Computer Center
(Linux farm). PyPWA extract model parameters from data by performing
extended likelihood fits. Two versions of the software are develop: one
where general amplitudes (or any parametric model) can be used in the fit
and simulation of data, and a second where the framework starts with a
specific realization of the Isobar model, including extensions to
Deck-type and baryon vertices corrections.

Tutorials (Step-by-step instructions) leading to a full fit of data and
the use of simulation software are included. Most of the code is in Python, but
hybrid code (in Cython or Fortran) has been used when appropriate.
Scripting to make use of vectorization and parallel coprocessors
(Xeon-Phi and/or GPUs) are expected in the near future. The goal of this
software framework is to create a user friendly environment for the
spectroscopic analysis of linear polarized photoproduction experiments.
The PyPWA Project software expects to be in a continue flow
(of improvements!), therefore, please check on the more recent software
download version.


What can PyPWA do?
------------------

 - Likelihood fitting with ChiSquared and Log Likelihood
 - Simulation using the Monte-Carlo Rejection Sampling method
 - Multi-variable binning for 4 vector particle data (in GAMP Format)
 - Convert and mask data between similar data types
 - Load data into an HDF5 dataset



Further Reading
---------------

 - `iMinuit <https://iminuit.readthedocs.io/en/latest/index.html>`_
 - `Nestle <http://kylebarbary.com/nestle/>`_
 - `PyTables (HDF5) <https://www.pytables.org/index.html>`_



.. include:: ../../../CONTRIBUTORS.rst
