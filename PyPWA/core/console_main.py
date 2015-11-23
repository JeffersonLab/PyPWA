"""
Main objects for console PyPWA tools
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import PyPWA.data.file_manager, PyPWA.proc.calculation_tools, PyPWA.proc.calculation

class Fitting(object):
    """Main General Fitting Object
    Args:
        config (dict): A dictionary with all the configuration packed into it.
        cwd (str): The current working directory for the application
    """

    def __init__(self, config, cwd):
        self.generated_length = config["Likelihood Information"]["Generated Length"]
        self.function_location = config["Likelihood Information"]["Function's Location"]
        self.amplitude_name = config["Likelihood Information"]["Processing Name"]
        self.setup_name = config["Likelihood Information"]["Setup Name"]
        self.data_location = config["Data Information"]["Data Location"]
        self.accepted_location = config["Data Information"]["Accepted Monte Carlo Location"]
        self.qfactor_location = config["Data Information"]["QFactor List Location"]
        self.initial_settings = config["Minuit's Settings"]["Minuit's Initial Settings"]
        self.parameters = config["Minuit's Settings"]["Minuit's Parameters"]
        self.strategy = config["Minuit's Settings"]["Minuit's Strategy"]
        self.set_up = config["Minuit's Settings"]["Minuit's Set Up"]
        self.ncall = config["Minuit's Settings"]["Minuit's ncall"]
        self.num_threads = config["General Settings"]["Number of Threads"]
        self.use_qfactor = config["Generated Settings"]["Use QFactor"]
        self.cwd = cwd


    def start(self):
        """Starts fitting process"""

        print("Parsing files into memory.\n")
        parse = PyPWA.data.file_manager.MemoryInterface()
        data = parse.parse(self.data_location)
        accepted = parse.parse(self.accepted_location)
        if self.use_qfactor:
            qfactor = parse.parse(self.qfactor_location)
        else:
            qfactor = numpy.ones(shape=len(data.values()[0]))

        print("Loading users function.\n")
        functions = PyPWA.proc.calculation_tools.FunctionLoading(self.cwd, self.function_location, self.amplitude_name, self.setup_name)
        amplitude_function = functions.return_amplitude()
        setup_function = functions.return_setup()

        calc = PyPWA.proc.calculation.MaximumLogLikelihoodEstimation(self.num_threads, self.parameters, data, accepted, qfactor, self.generated_length, amplitude_function, setup_function)
        minimalization = PyPWA.proc.calculation_tools.Minimalizer(calc.run, self.parameters, self.initial_settings, self.strategy, self.set_up, self.ncall)

        print("Starting minimalization.\n")
        minimalization.min()
        calc.stop()


class Simulator(object):
    """Main General Simulator Object
    Args:
        config (dict): A dictionary with all the configuration packed into it.
        cwd (str): The current working directory for the application
    """

    def __init__(self, config, cwd):
        self.function_location = config["Simulator Information"]["Function's Location"]
        self.amplitude_name = config["Simulator Information"]["Processing Name"]
        self.setup_name = config["Simulator Information"]["Setup Name"]
        self.parameters = config["Simulator Information"]["Parameters"]
        self.num_threads = config["Simulator Information"]["Number of Threads"]
        self.data_location = config["Data Information"]["Monte Carlo Location"]
        self.save_location = config["Data Information"]["Save Location"]
        self.cwd = cwd


    def start(self):
        """Starts Rejection"""

        print("Parsing data into memory.\n")
        data_manager = PyPWA.data.file_manager.MemoryInterface()
        data = data_manager.parse(self.data_location)

        print("Loading users functions.\n")
        functions = PyPWA.proc.calculation_tools.FunctionLoading(self.cwd, self.function_location, self.amplitude_name, self.setup_name )
        amplitude_function = functions.return_amplitude()
        setup_function = functions.return_setup()

        print("Running Simulation")
        rejection_method = PyPWA.proc.calculation.AcceptanceRejctionMethod( self.num_threads, data, amplitude_function, setup_function, self.parameters)

        rejection_list = rejection_method.run()

        print("Saving Data")
        data_manager.write(self.save_location, rejection_list )


class Configurations(object):
    """Static class that returns the example txt"""

    @staticmethod
    def fitting_config():
        """
        Retruns:
            str: Example.yml for GeneralFitting
        """
        return """\
Likelihood Information: #There must be a space bewteen the colon and the data
    Generated Length : 10000   #Number of Generated events
    Function's Location : Example.py   #The python file that has the functions in it
    Processing Name : the_function  #The name of the processing function
    Setup Name :  the_setup   #The name of the setup function, called only once before fitting
Data Information:
    Data Location : /home/user/foobar/data.txt #The location of the data
    Accepted Monte Carlo Location: /home/foobar/fit/AccMonCar.txt   #The location of the Accepted Monte Carlo
    QFactor List Location : /home/foobar/fit/Qfactor.txt #The location of the Qfactors
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
    Use QFactor: True   #Boolean, using Qfactor or not
"""


    @staticmethod
    def simulator_config():
        """
        Returns:
            str: Example.yml for GeneralSimulator
        """
        return """\
Simulator Information: #There must be a space bewteen the colon and the data
    Function's Location : Example.py   #The python file that has the functions in it
    Processing Name : the_function  #The name of the processing function
    Setup Name :  the_setup   #The name of the setup function, called only once before fitting
    Parameters : { A1: 1, A2: 2, A3: 0.1, A4: -10, A5: -0.00001 }
    Number of Threads: 2
Data Information:
    Monte Carlo Location : /home/user/foobar/data.txt #The location of the data
    Save Location : /home/user/foobabar/weights.txt #Where you want to save the weights
    """


    @staticmethod
    def example_function():
        """
        Returns:
            str: Example.py for both GeneralShell tools.
        """
        return """\
import numpy

def the_function(the_array, the_params): #You can change both the variable names and function name
    the_size = len(the_array.values()[0]) #You can change the variable name here, or set the length of values by hand
    values = numpy.zeros(shape=the_size)
    for x in range(the_size):
        #Here is where you define your function.
        #Your array has to have a [x] after it so the for loop can iterate through all the events in the array
        values[x] = the_param["A1"] + the_array["kvar"][x]
    return values

def the_setup(): #This function can be renamed, but will not be sent any arguments.
    #This function will be ran once before the data is Minuit begins.
    pass
"""
