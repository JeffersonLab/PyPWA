
############
Installation
############
PyPWA doesn't have distribution specific packages yet, so for the time
being you will have to rely on pip. These steps will walk you through how to
install Python to your machine using Pip.


Installing Dependencies
#######################
You need some packages installed to your machine in order to use PyPWA.

.. note::
   You can skip this if you don't have administrative access to your machine,
   though the installation might be more error prone.

**Arch Linux:**

.. code-block:: sh

   sudo pacman -S base-devel python-virtualenv python-scipy python-numpy


**Debian 8+ / Ubuntu 14.04 LTS+:**

.. code-block:: sh

   sudo apt update
   sudo apt install build-essential virtualenv python3-scipy python3-numpy


**CentOS 7 / RedHat 7:**

.. code-block:: sh

   sudo yum groupinstall "Development Tools"
   sudo yum python-virtualenv scipy numpy


**Fedora 21+:**

.. code-block:: sh

   sudo dnf group install "Development Tools"
   sudo dnf install python3-virtualenv python3-scipy python3-numpy


Install PyPWA
#############
It is not recommended to install PyPWA systemwide, please wait until we are in
a position to start producing PKGBUILD, .debs, and .rpms to distribute the
package.

To install, choose between:
   A. your home directory:

      .. warning::
         If there is a quota on your home directory, this could overflow it.

      .. code-block:: sh

         pip install --user git+https://github.com/JeffersonLab/PyPWA.git

   B. anywhere with a virtual environment:

      .. tip::
         If you are using TCSH, you need to ``source venv/bin/activate.csh``
         instead.

      .. code-block:: sh

         virtualenv --system-site-packages venv
         source venv/bin/activate
         pip install git+https://github.com/JeffersonLab/PyPWA.git
