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

import PyPWA.data, PyPWA.proc.likelihood, PyPWA.minuit, click, sys, numpy

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
    def start(self):
        """
        Actually runs all the data, not the best way of doing things but it works, functions as the main function of the program running all the other functions of the program.
        """

        with click.progressbar(length=5, label="Configuring GeneralFitting") as progress:
            self.data = PyPWA.data.Interface()
            progress.update(1)
            self.minimalization = PyPWA.minuit.Minimalizer(self.config["Minuit's Settings"])
            progress.update(1)
            self.calc = PyPWA.proc.likelihood.Calc(self.config["Likelihood Information"])
            progress.update(1)
            self.calc.general = self.config["General Settings"]
            progress.update(1)
            self.calc.parameters = self.config["Minuit's Settings"]["Minuit's Parameters"]
            progress.update(1)

        self.calc.data = self.data.parse(self.config["Data Information"]["Data Location"])
        self.calc.accepted = self.data.parse(self.config["Data Information"]["Accepted Monte Carlo Location"])
        self.calc.qfactor = self.data.parse(self.config["Data Information"]["QFactor List Location"])
        self.calc.prep_work()

        click.secho("Starting iminiut.")
        self.minimalization.calc_function = self.calc.run
        self.minimalization.min()
        self.calc.stop()
    
class Simulator(object): #Todo: Clean Up Josh's code
    example_function = """\
def the_function(the_array, the_params):
        the_size = len(the_array.values()[0]) #You can change the variable name here, or set the length of values by hand
    values = numpy.zeros(shape=the_size)
    for x in range(the_size):
        #    This is where you define your intensity function. Do not change the name of the function. 
        #    The names of the arguments are up to you, but they both need to be dictionaries, with the 
        #    first one being the kinematic variables, either from a gamp event or a list. And the second
        #    being the fitted parameters. All fitted parameters need to be floating point numbers. If a
        #    parameter of your function is a complex number make the real part one fitted variable and
        #    the imaginary part another. Your function should return a float. 
        values[x] = (the_array['s'][x]**2)*(the_array['t'][x]**3)*the_params["A1"] #example
    return values

    
    return (kVars['s']**2)*(kVars['t']**3)*params["A1"] #example
    """
    example_config_simulator = """\
Simulator:
    nTrue file: ntrue.txt
    Input kinematic variables file: kvar.txt
    Output Weight file: output.txt
    Intensities file: ilist.npy
    Maximum intensity of whole mass range file: maxMass.npy
"""
    example_config_calcIlist = """\
Calculate List of intensities:
    Function Location: Example.py
    Function Name: intFn
    Input kinematic variables file: kvar.txt
    Parameters: {'A1':7.,'A2':-3.0,'A3':0.37,'A4':0.037,'A5':0.121}
    Save location: ilist.npy
"""
    simulator_config = None
    calcIlist_config = None
    cwd = None

    def calcIlist(self):
        sys.path.append(self.cwd)
        imported = __import__(self.calcIlist_config["Function Location"].strip(".py"))
        users_function = getattr(imported, self.calcIlist_config["Function Name"])

        data = PyPWA.data.Interface()
        kvar = data.parse(self.calcIlist_config["Input kinematic variables file"])
        numpy.save( self.calcIlist_config["Save location"], users_function(kvar, self.calcIlist_config["Parameters"]))

    def Simulate(self):
        iList = numpy.load(self.simulator_config["Intensities file"])
        iMax = numpy.load(self.simulator_config["Maximum intensity of whole mass range file"])

        nTrueList = [((1.0/(iList.shape[0]))*(iList.sum(0)))]
        numpy.save(self.simulator_config["nTrue file"],nTrueList)

        wList = iList[:]/iMax

        wnList = numpy.zeros(shape=(wList.shape[0]))

        for wn in range(len(wList)):
            if wList[wn] > numpy.random.random():
                wnList[wn] = 1

        numpy.save(self.simulator_config["Output Weight file"], wnList)