
#################
Environment Setup
#################
The purpose of this documentation is to help new developers get up to speed
quickly with contributing to PyPWA. This should be able to take your favorite
Linux box and set it up with a Python Development Environment and PyPWA
ready to be worked on.

The two different ways to install a development environment on your machine:
   A. The Virtualenv instructions uses your systems packages to create a
      virtual environment that supports both Bash and CSH.
   B. The Anaconda instructions will have you installing Anaconda or
      Miniconda onto your system, then using the Conda environment for your
      development.

.. caution::
  Your shell determines which method you can use. You can tell what your
  shell is by opening a terminal and running ``echo $SHELL`` which should
  give you a path to your current shell. Most Linuxes default to Bash, 
  but JLab and BSD default to TCSH instead.


.. toctree::
   :maxdepth: 2

   virt
   conda

