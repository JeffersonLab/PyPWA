
##############
Setting up Git
##############
PyPWA's source code is hosted inside Github, a service designed for the
management of software projects online, and in order to access it you will need
to use Git. This section will walk you through installing Git, setting up a
project directory, downloading PyPWA's source, and then switching to the
development branch.


Installing Git
##############

**Arch Linux:**

.. code-block:: sh

   sudo pacman -Sy git


**Debian / Ubuntu:**

.. code-block:: sh

   sudo apt update
   sudo apt install git


**Fedora:**

.. code-block:: sh

   sudo dnf install git


**Redhat / CentOS:**

.. code-block:: sh

   sudo yum install git


Getting PyPWA's Source
######################

Navigate in your terminal to where you want PyPWA to be, then run the following
Git command:

.. code-block:: sh

   cd $PROJECT/
   git clone git@github.com:JeffersonLab/PyPWA.git --branch development

We specifiy the ``development`` branch here because our development is our
working branch while the master branch is reserved exclusively for releases.

