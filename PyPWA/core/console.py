"""
GeneralFitting.py: The GeneralShell, provides users a flexible way of testing their calcutions
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Alpha"

import PyPWA.data, PyPWA.proc.likelihood, PyPWA.iminuit, click

class Fitting(object):
    """
    Main point of entry into the General Shell, trying to stay as pythonic as possible.
    Tries to be both intelligent and provide a flexible way for users to do what they want how they want.
    """

    config = None

    example_config = """\
Likelihood Information:
    Generated Length : 10000   #Number of Generated events
    Function's Location : Example.py   #The python file that has the functions in it
    Processing Name : the_function  #The name of the processing function
    Setup Name :  the_setup   #The name of the setup function, called only once before fitting
Data Information:
    Data Location : /home/user/foobar/data.txt #The location of the data
    Accepted Monte Carlo Location: /home/foobar/fit/AccMonCar.txt   #The location of the Accepted Monte Carlo
    QFactor List Location : /home/foobar/fit/Qfactor.txt #The location of the Qfactors
Minuit's Settings:
    Minuit's Initial Settings : { A1: 1, A2: 2, A3: 0.1, A4: -10, A5: -0.00001, limit_A1: [0, 2500] }  #Iminuit settings in a single line
    Minuit's Parameters: [ A1, A2, A3, A4, A5 ]   #The name of the Parameters passed to Minuit
    Minuit's Strategy : 1
    Minuit's Set Up: 0.5
    Minuit's ncall: 1000
General Settings:
    Number of Threads: 1   #Number of threads to use. Set to one for debug
    Use QFactor: True   #Boolean, using Qfactor or not
"""

    example_function = """\
import numpy

def the_function(the_array, the_params): #You can change both the variable names and function name
    the_size = len(the_array.values()[0]) #You can change the variable name here, or set the length of values by hand
    values = numpy.zeros(shape=the_size)
    for x in range(the_size):
        #Here is where you define your function.
        values[x] = the_param["A1"] + the_array["kvar"][x]
    return values

def the_setup(): #This function can be renamed, but will not be sent any arguments.
    #This function will be ran once before the data is Minuit begins.
    pass
"""
    def start(self, config):
        """
        Actually runs all the data, not the best way of doing things but it works, functions as the main function of the program running all the other functions of the program.
        """

        with click.progressbar(length=4, label="Configuring GeneralFitting") as progress:
            self.data = PyPWA.data.Interface()
            progress.update(1)
            self.minimalization = PyPWA.iminiut.Minimalizer(self.config["Minuit's Settings"])
            progress.update(1)
            self.calc = PyPWA.calc.likelihood.Calc(self.config["Likelihood Information"])
            progress.update(1)
            self.calc.general = self.config["General Settings"]
            progress.update(1)

        self.data.parse(self.config["Data Information"]["Data Location"])
        self.calc.data = self.data.parsed
        self.data.parse(self.config["Data Information"]["Accepted Monte Carlo"])
        self.calc.accepted = self.data.parsed
        self.data.parse(self.config["Data Information"]["QFactor List Location"])
        self.calc.qfactor = self.data.parsed
        self.calc.prepwork()

        click.secho("Starting iminiut.")
        self.minimalization(self.config["iminuit"])
        self.minimalization.calc_function = self.calc.run()
        self.minimalization.test()
        self.minimalization.min()
    