General Fitting 
========================
Section 1.1
------------------------

:Authors: C. Salgado, L.M.Hare

:Version: 1.0 of 08/01/2016

:Dedication: To my Beautiful Wife Patrice.

	This tutorial is being written to compliment and assist with the use of the General Fitting model through the Computational Computing. This can be used either through a desktop or through the interactive computing farm. 

	1) First create a directory which should be named after the experiment that was completed. (For the purposes of this Tutorial we shall use "MAIN".)
		a- All data should be located in this directory. 
		b- Ensure that you keep track of where this directory. 
	2) Copy the programs files from the following site: https://github.com/JeffersonLab/PyPWA/releases. 
		a- The latest version is called PyPWA-<version>.tar.gz will need to be installed.
	3) To install run "pip install --user PyPWA-<version>.tar.gz". Omit quotes.
	4) Run General Fitting -wc
::

		a- This will create 2 files: 
		Example.py
		Example.yml
		b- Rename Example.py to MAIN.py.
		c- Rename Example.yml to MAIN.yml
-------------

	5) Within the MAIN.yml is the configuration file for the actual computational process. You must edit::

			Generated Length
			Function Length
			Processing Name
			Set Up Name
			Data Location
			Save Name
			Minuit Settings
			General Setting

			a- Within this configuration file, there are several parameters that must be set before the program can be run. Several of the 				parameters can be set to be exempt from being run by using the "#" before the desired parameter. This will prevent that parameter 				from being used within the process. 
	
