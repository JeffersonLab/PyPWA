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

import os
import warnings

import numpy
import tabulate

import PyPWA.data.file_manager
from PyPWA.proc import calculation_tools, calculation


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

        if "Accepted Monte Carlo Location" in config["Data Information"]:
            self.accepted_location = config["Data Information"]["Accepted Monte Carlo Location"]
        else:
            self.accepted_location = None

        if "QFactor List Location" in config["Data Information"]:
            self.QFactor_location = config["Data Information"]["QFactor List Location"]
        else:
            self.QFactor_location = None

        self.save_location = config["Data Information"]["Save Name"]

        self.initial_settings = config["Minuit's Settings"]["Minuit's Initial Settings"]
        self.parameters = config["Minuit's Settings"]["Minuit's Parameters"]
        self.strategy = config["Minuit's Settings"]["Minuit's Strategy"]
        self.set_up = config["Minuit's Settings"]["Minuit's Set Up"]
        self.ncall = config["Minuit's Settings"]["Minuit's ncall"]
        self.num_threads = config["General Settings"]["Number of Threads"]
        self.cwd = cwd

    def start(self):
        """Starts fitting process"""

        print("Parsing files into memory.\n")
        parse = PyPWA.data.file_manager.MemoryInterface()
        data = parse.parse(self.data_location)

        if not isinstance(self.accepted_location, type(None)):
            accepted = parse.parse(self.accepted_location)

        new_data = {}
        new_accepted = {}

        if not isinstance(self.QFactor_location, type(None)):
            if "QFactor" in data and os.path.isfile(self.QFactor_location):
                QFactor = parse.parse(self.QFactor_location)
                if QFactor != data["QFactor"]:
                    raise Exception("Two different QFactors were provided! Remove a QFactor set and retry.")

        if "QFactor" in data:
            new_data["QFactor"] = data["QFactor"]
            data.pop("QFactor")
        elif not isinstance(self.QFactor_location, type(None)):
            new_data["QFactor"] = parse.parse(self.QFactor_location)
        else:
            warnings.warn("QFactor data not found! Continuing on without QFactor.")
            new_data["QFactor"] = numpy.ones(shape=len(data[data.keys()[0]]))

        if "BinN" in data:
            new_data["BinN"] = data["BinN"]
            data.pop("BinN")
        else:
            new_data["BinN"] = numpy.ones(shape=len(data[data.keys()[0]]))

        new_data["data"] = data

        if not isinstance(self.accepted_location, type(None)):
            if "BinN" in accepted:
                new_accepted["BinN"] = accepted["BinN"]
                accepted.pop("BinN")
            else:
                new_accepted["BinN"] = numpy.ones(shape=len(accepted[accepted.keys()[0]]))
        else:
            accepted = 0

        new_accepted["data"] = accepted

        print("Loading users function.\n")
        functions = calculation_tools.FunctionLoading(self.cwd, self.function_location, self.amplitude_name,
                                                      self.setup_name)
        amplitude_function = functions.return_amplitude
        setup_function = functions.return_setup


        if isinstance(self.accepted_location, type(None)):
            calc = calculation.MaximumLogLikelihoodUnextendedEstimation(self.num_threads, self.parameters, new_data,
                                                                        amplitude_function, setup_function)
        else:
            calc = calculation.MaximumLogLikelihoodExtendedEstimation(self.num_threads, self.parameters, new_data,
                                                                      new_accepted, self.generated_length,
                                                                      amplitude_function, setup_function)

        calc = calculation.ChiSquaredTest(self.num_threads, self.parameters, new_data, amplitude_function,
                                          setup_function)

        minimization = calculation_tools.Minimizer(calc.run, self.parameters, self.initial_settings, self.strategy,
                                                   self.set_up, self.ncall)

        print("Starting minimization.\n")
        minimization.min()
        calc.stop()

        if not isinstance(minimization.covariance, type(None)):
            print("Covariance.\n")
            the_x = []
            the_y = []
            for field in minimization.covariance:
                the_x.append(field[0])
                the_y.append(field[1])

            x_true = set(the_x)
            y_true = set(the_y)

            covariance = []
            for x in x_true:
                holding = [x]
                for y in y_true:
                    holding.append(minimization.covariance[(x, y)])
                covariance.append(holding)

            table_fancy = tabulate.tabulate(covariance, y_true, "fancy_grid", numalign="center")
            table = tabulate.tabulate(covariance, y_true, "grid", numalign="center")

            try:
                print(table_fancy)
            except UnicodeEncodeError:
                try:
                    print(table)
                except:
                    pass

            with open( self.save_location + ".txt", "w") as stream:
                stream.write("Covariance.\n")
                stream.write(table)
                stream.write("\n")
                stream.write("fval: "+str(minimization.fval))

            numpy.save(self.save_location + ".npy", {"covariance": minimization.covariance, "fval": minimization.fval,
                                                     "values": minimization.values})


class Chi(object):
    """Main General Fitting Object
    Args:
        config (dict): A dictionary with all the configuration packed into it.
        cwd (str): The current working directory for the application
    """

    def __init__(self, config, cwd):
        self.function_location = config["ChiSquared Information"]["Function's Location"]
        self.amplitude_name = config["ChiSquared Information"]["Processing Name"]
        self.setup_name = config["ChiSquared Information"]["Setup Name"]

        self.data_location = config["Data Information"]["Data Location"]

        if "QFactor List Location" in config["Data Information"]:
            self.QFactor_location = config["Data Information"]["QFactor List Location"]
        else:
            self.QFactor_location = None

        self.save_location = config["Data Information"]["Save Name"]

        self.initial_settings = config["Minuit's Settings"]["Minuit's Initial Settings"]
        self.parameters = config["Minuit's Settings"]["Minuit's Parameters"]
        self.strategy = config["Minuit's Settings"]["Minuit's Strategy"]
        self.set_up = config["Minuit's Settings"]["Minuit's Set Up"]
        self.ncall = config["Minuit's Settings"]["Minuit's ncall"]
        self.num_threads = config["General Settings"]["Number of Threads"]
        self.cwd = cwd

    def start(self):
        """Starts fitting process"""

        print("Parsing files into memory.\n")
        parse = PyPWA.data.file_manager.MemoryInterface()
        data = parse.parse(self.data_location)

        if not isinstance(self.accepted_location, type(None)):
            accepted = parse.parse(self.accepted_location)

        new_data = {}
        new_accepted = {}

        if not isinstance(self.QFactor_location, type(None)):
            if "QFactor" in data and os.path.isfile(self.QFactor_location):
                QFactor = parse.parse(self.QFactor_location)
                if QFactor != data["QFactor"]:
                    raise Exception("Two different QFactors were provided! Remove a QFactor set and retry.")

        if "QFactor" in data:
            new_data["QFactor"] = data["QFactor"]
            data.pop("QFactor")
        elif not isinstance(self.QFactor_location, type(None)):
            new_data["QFactor"] = parse.parse(self.QFactor_location)
        else:
            warnings.warn("QFactor data not found! Continuing on without QFactor.")
            new_data["QFactor"] = numpy.ones(shape=len(data[data.keys()[0]]))

        new_data["BinN"] = data["BinN"]
        data.pop("BinN")

        new_data["data"] = data


        print("Loading users function.\n")
        functions = calculation_tools.FunctionLoading(self.cwd, self.function_location, self.amplitude_name,
                                                      self.setup_name)
        amplitude_function = functions.return_amplitude
        setup_function = functions.return_setup

        calc = calculation.ChiSquaredTest(self.num_threads, self.parameters, new_data, amplitude_function,
                                          setup_function)

        minimization = calculation_tools.Minimizer(calc.run, self.parameters, self.initial_settings, self.strategy,
                                                   self.set_up, self.ncall)

        print("Starting minimization.\n")
        minimization.min()
        calc.stop()

        if not isinstance(minimization.covariance, type(None)):
            print("Covariance.\n")
            the_x = []
            the_y = []
            for field in minimization.covariance:
                the_x.append(field[0])
                the_y.append(field[1])

            x_true = set(the_x)
            y_true = set(the_y)

            covariance = []
            for x in x_true:
                holding = [x]
                for y in y_true:
                    holding.append(minimization.covariance[(x, y)])
                covariance.append(holding)

            table_fancy = tabulate.tabulate(covariance, y_true, "fancy_grid", numalign="center")
            table = tabulate.tabulate(covariance, y_true, "grid", numalign="center")

            try:
                print(table_fancy)
            except UnicodeEncodeError:
                try:
                    print(table)
                except:
                    pass

            with open(self.save_location + ".txt", "w") as stream:
                stream.write("Covariance.\n")
                stream.write(table)
                stream.write("\n")
                stream.write("fval: "+str(minimization.fval))

            numpy.save(self.save_location + ".npy", {"covariance": minimization.covariance, "fval": minimization.fval,
                                                     "values": minimization.values})


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
        data_manager = PyPWA.data.file_manager.MemoryInterface(True)
        data = data_manager.parse(self.data_location)

        print("Loading users functions.\n")
        functions = calculation_tools.FunctionLoading(self.cwd, self.function_location, self.amplitude_name,
                                                      self.setup_name)
        amplitude_function = functions.return_amplitude
        setup_function = functions.return_setup

        print("Running Intensities")
        intensities = calculation.CalculateIntensities(self.num_threads, data, amplitude_function,
                                                       setup_function, self.parameters)

        intensities_list, max_intensity = intensities.run()

        print("Running Acceptance Rejection")
        rejection = calculation.AcceptanceRejectionMethod(intensities_list, max_intensity)

        rejection_list = rejection.run()

        print("Saving Data")
        data_manager.write(self.save_location, rejection_list)


class Intensities(object):
    def __init__(self, config, cwd):
        self.function_location = config["Intensities Information"]["Function's Location"]
        self.amplitude_name = config["Intensities Information"]["Processing Name"]
        self.setup_name = config["Intensities Information"]["Setup Name"]
        self.parameters = config["Intensities Information"]["Parameters"]
        self.num_threads = config["Intensities Information"]["Number of Threads"]
        self.data_location = config["Data Information"]["Monte Carlo Location"]
        self.save_location = config["Data Information"]["Save Location"]
        self.cwd = cwd

    def start(self):
        print("Parsing data into memory.\n")
        data_manager = PyPWA.data.file_manager.MemoryInterface(True)
        data = data_manager.parse(self.data_location)

        print("Loading users functions.\n")
        functions = calculation_tools.FunctionLoading(self.cwd, self.function_location, self.amplitude_name,
                                                      self.setup_name)
        amplitude_function = functions.return_amplitude
        setup_function = functions.return_setup

        print("Running Intensities")
        intensities = calculation.CalculateIntensities(self.num_threads, data, amplitude_function, setup_function,
                                                       self.parameters)

        intensities_list, max_intensity = intensities.run()

        print("Saving Data")
        data_manager.write(self.save_location, intensities_list)


class Weights(object):
    def __init__(self, config, cwd):
        self.max_intensity = config["Max Intensity"]
        self.intensities_location = config["Intensities Location"]
        self.save_location = config["Save Location"]
        self.cwd = cwd

    def start(self):
        print("Parsing data into memory.\n")
        data_manager = PyPWA.data.file_manager.MemoryInterface(True)
        data = data_manager.parse(self.intensities_location) 

        print("Running Acceptance Rejection")
        rejection = calculation.AcceptanceRejectionMethod(data, self.max_intensity)

        rejection_list = rejection.run()

        print("Saving Data")
        data_manager.write(self.save_location, rejection_list)


class Configurations(object):
    """Static class that returns the example txt"""

    @staticmethod
    def fitting_config():
        """
        Returns:
            str: Example.yml for GeneralFitting
        """
        return """\
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
"""

    @staticmethod
    def chi_config():
        """
        Returns:
            str: Example.yml for GeneralFitting
        """
        return """\
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
    Save Location : /home/user/foobar/weights.txt #Where you want to save the weights
"""

    @staticmethod
    def intensities_config():
        return """\
Intensities Information : #There must be a space bewteen the colon and the data
    Function's Location : Example.py   #The python file that has the functions in it
    Processing Name : the_function  #The name of the processing function
    Setup Name :  the_setup   #The name of the setup function, called only once before fitting
    Parameters : { A1: 1, A2: 2, A3: 0.1, A4: -10, A5: -0.00001 }
    Number of Threads: 2
Data Information:
    Monte Carlo Location : /home/user/foobar/data.txt #The location of the data
    Save Location : /home/user/foobar/weights.txt #Where you want to save the intensities
"""

    @staticmethod
    def weights_config():
        return """\
Max Intensity : 2.78964398923 #The max intensity for the entire data range.
Intensities Location :  /home/user/foobar/data.txt #The location of the intensities
Save Location: /home/user/foobar/weights.txt #The location of where to save the data for
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
    the_size = len(the_array[list(the_array)[0]) #You can change the variable name here, or set the length of values by hand
    values = numpy.zeros(shape=the_size)
    for event in range(the_size):
        #Here is where you define your function.
        #Your array has to have a [event] after it so the for loop can iterate through all the events in the array
        values[event] = the_params["A1"] + the_array["kvar"][event] #Change "kvar" to the name of your vairable, and "A1" to your parameter
    return values

def the_setup(): #This function can be renamed, but will not be sent any arguments.
    #This function will be ran once before the data is Minuit begins.
    pass
"""
# I hate this file too

