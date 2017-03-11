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

5) Within the MAIN.yml is the configuration file for the actual computational process. You will see::

	Likelihood Information: #There must be a space between the colon and the data
	    Generated Length : 10000   #Number of Generated events
	    Function's Location : Example.py   #The python file that has the functions in it
	    Processing Name : the_function  #The name of the processing function
	    Setup Name :  the_setup   #The name of the setup function, called only once before fitting
	Data Information:
	    Data Location : /home/user/foobar/data.txt #The location of the data
	#    Accepted Monte Carlo Location: /home/foobar/fit/AccMonCar.txt  # Optional, Path to your accepted data
	#    QFactor List Location : /home/foobar/fit/Qfactor.txt #Optional, The location of the QFactors
	    Save Name : output #Will make a file called output.txt and output.npy
	Minuit's Settings:
	    Minuit's Initial Settings : { A1: 1, limit_A1: [0, 2500], # You can arrange this value however you would like as long as the each line ends in either a "," or a "}"
	        A2: 2, limit_A2: [-2,3],
	        A3: 0.1, A4: -10,
	        A5: -0.00001 }  #Iminuit settings in a single line
	    Minuit's Parameters: [ A1, A2, A3, A4, A5 ]   #The name of the Parameters passed to Minuit
	    Minuit's Strategy : 1
	    Minuit's Set Up: 0.5
	    Minuit's ncall: 1000
	General Settings:
	    Number of Threads: 1   #Number of threads to use. Set to one for debug
	    Logging Level: warn  #Supports debug info warn
	
6) You must edit::	

	Generated Length
	Function Length
	Processing Name
	Set Up Name
	Data Location
	Save Name
	Minuit Settings
	General Setting

	a- Within this configuration file, there are several parameters that must be set before the program can be run. Several of the	parameters can be set to be exempt from being run by using the "#" before the desired parameter. This will prevent that parameter from being used within the process.
			
	b- Following this the process will begin running showing each calculation. Once completed, the program will create several tables showing the completed computations.
	
7) Within this program we can fit the data to the model that is given using the Chi function, for this you must again ensure that your data is within the same directory. 

8) You must run the the command "ChiSquared -wc". Omit quotes. 

9) This will create two files::

	Example.py
	Example.yml

10) You must rename the Example.yml to MAINChi.yml.

11) You must edit MAINChi.yml to the parameters of your experiment, you will see the following::

	ChiSquared Information: #There must be a space between the colon and the data
   		Function's Location : Example.py   #The python file that has the functions in it
    	Processing Name : the_function  #The name of the processing function
    	Setup Name :  the_setup   #The name of the setup function, called only once before fitting
	Data Information:
	    Data Location : /home/user/foobar/data.txt #The location of the data
	#    QFactor List Location : /home/foobar/fit/Qfactor.txt #Optional, The location of the QFactors
	    Save Name : output #Will make a file called output.txt and output.npy
	Minuit's Settings:
	    Minuit's Initial Settings : { A1: 1, limit_A1: [0, 2500], # You can arrange this value however you would like as long as the each line ends in either a "," or a "}"
	        A2: 2, limit_A2: [-2,3],
	        A3: 0.1, A4: -10,
	        A5: -0.00001 }  #Iminuit settings in a single line
	    Minuit's Parameters: [ A1, A2, A3, A4, A5 ]   #The name of the Parameters passed to Minuit
	    Minuit's Strategy : 1
	    Minuit's Set Up: 0.5
	    Minuit's ncall: 1000
	General Settings:
	    Number of Threads: 1   #Number of threads to use. Set to one for debug
	    Logging Level: warn  #Supports debug info warn

12 You must edit::

    ChiSquared Information
    Function's Location
    Processing Location
    Data Information
    Minuit's Initial Settings
    Minuit's Strategy
    Minuit's Set Up
    Minuit's ncall
    Number of Threads
	- You must enter your data location via it's absolute path. 
	- The data must be in one of 3 forms::
		- Comma Seperated Variable Sheet
		- Tab Seperated Variable Sheet
		- EVIL
	- It must be in a text file.

13) Once complete, run the command "GeneralChiSquared MAINChi.yml".

14) This will begin the computations.

15) Once this has completed a set of tables will be created with the computations. 
		