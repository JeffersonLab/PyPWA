
##########
Virtualenv
##########
Virtualenv will create a folder inside a specified directory, symlink Python,
and the site packages into that folder to be used for the specific folder.
It is the best way to test that the package will work on a specific Unix system
without Anaconda and without installing the package to the system directly.

.. caution::
   ``sudo`` access is required to install Virtualenv and PyPWA's dependencies,
   however it is not needed to create the environment itself.


Installing Software
###################
You must have Git, Fortran, and Virtualenv installed for the environment to
work correctly. Follow the instructions below for your distribution of Linux
for all packages to be installed correctly. You must have Python 2.7+ or
Python 3.4+ for PyPWA to work correctly.

**Arch Linux:**

.. code-block:: sh

   sudo pacman -S base-devel gcc-fortran python-virtualenv


**Debian 8+ / Ubuntu 14.04 LTS+:**

.. code-block:: sh

   sudo apt update
   sudo apt install build-essential gfortran virtualenv


**CentOS 7 / RedHat 7:**

.. code-block:: sh

   sudo yum install epel-release
   sudo yum groupinstall "Development Tools"
   sudo yum install gcc-gfortran python-virtualenv


**Fedora 21+:**

.. code-block:: sh

   sudo dnf group install "Development Tools"
   sudo dnf install gcc-gfortran python3-virtualenv


Creating a Virtualenv environment
#################################
I am going to use ``venv`` as the name for the environment in this example
because some editors default to searching for a ``venv`` environment directory,
however you are free to change this as you like.

**Make the environment folder:**

.. code-block:: sh

   cd $PROJECT/PyPWA
   virtualenv venv --system-site-packages

**Activate the environment:**

Bash Family:

.. code-block:: sh

   source venv/bin/activate

CSH Family:

.. code-block:: sh

   source venv/bin/activate.csh


**Update setuptools:**

.. code-block:: sh

   pip install --upgrade setuptools


**Install PyPWA in development mode:**

.. code-block:: sh

   pip install -e $PROJECT/PyPWA/.
