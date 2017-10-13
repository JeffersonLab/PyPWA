
##############
Setting up Git
##############
PyPWA's source code is hosted inside Github, a service designed for the
management of software projects online, and in order to access it you will need
to use Git. This section will walk you through installing Git, setting up a
project directory, downloading PyPWA's source, and then switching to the
development branch.

**************
Installing Git
**************

**Arch Linux:**
::
   sudo pacman -Sy git


**Debian / Ubuntu:**
::
   sudo apt update
   sudo apt install git


**Fedora:**
::
   sudo dnf install git


**Redhat / CentOS:**
::
   sudo yum install git


**********************
Getting PyPWA's Source
**********************

Navigate in your terminal to where you want PyPWA to be, then run the following
Git command:
::
   cd $PROJECT/
   git clone git@github.com:JeffersonLab/PyPWA.git --branch development

We specify the ``development`` branch explicitily here because contributions
are only allowed directly to this branch unless there is a good reason to
contribute to the master branch such as fatal bug issues.
