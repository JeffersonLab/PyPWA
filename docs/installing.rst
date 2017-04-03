.. _installing-pypwa:

.. _Intel's Python: https://software.intel.com/en-us/intel-distribution-for-python
.. _virtualenv: https://virtualenv.pypa.io/en/stable/installation/
.. _Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _GitHub: https://github.com/JeffersonLab/PyPWA
.. _here: https://github.com/JeffersonLab/PyPWA/releases/download/v2.0.0-rc5/PyPWA-2.0.0rc5-py2.py3-none-any.whl
.. _releases: https://github.com/JeffersonLab/PyPWA/releases
.. _Anaconda: https://www.continuum.io/downloads


Installation
============
PyPWA is tested against Python 2.7, Python 3.3+, `Intel's Python`_, and
`Anaconda`_ to ensure compatibility.
We have also tested PyPWA on Cent-OS 6 & 7, the latest version of Fedora,
Arch Linux, and Debian.

.. note::
  Even if we don't test our package on your distribution, our package will
  likely work on your system as our package is almost entirely pure-python,
  with only a few non-pure-python dependencies.


Installing on your local machine using pip
------------------------------------------

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

Debian based distributions.
::
  $ sudo apt install python-dev gcc

Fedora 22 and later.
::
  $ sudo dnf install python-devel gcc

Arch Linux.
::
  $ sudo pacman -Su python gcc

Downloading and installing the Python Wheel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Download the current package from `here`_.

.. note::
  You can find the latest version of PyPWA along with older versions and
  their release notes on our `releases`_ page. Just look for the version you
  want and download its associated PyPWA*.whl file.


Navigate to where you downloaded the package file, then install the
package using pip.::
  $ sudo pip install PyPWA*.whl

.. note::
  You can install the package in your home directory without needing super
  user permissions, using ``$ pip install --user PyPWA*.whl`` instead.


Installing locally using Virtualenv
-----------------------------------
You will still need the listed dependencies listed above in
`Installing Dependencies`_ in order to use a virtualenv.

Before you begin, you will need to install `virtualenv`_ using the
instructions on their documentation.

  

Installing on your local machine using SetupTools
-------------------------------------------------

Before you begin, start by referencing `Installing Dependencies`_ above to
install the needed packages.

Download the source from our `GitHub`_ using `Git`_ somewhere you have write
permissions, then cd into the package.

Once inside the pacakge, run:
::
  $ sudo python setup.py install

Or alternatively to install just in your home folder:
::
  $ python setup.py install --local
