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

import os, iminuit, sys, PyPWA.data.KvData, PyPWA.processing.DataCalc

class GeneralFitting(object):
    """
    Main point of entry into the General Shell, trying to stay as pythonic as possible.
    Tries to be both intelligent and provide a flexible way for users to do what they want how they want.
    """

    def __init__(self, config):
        """
        Actually runs all the data, not the best way of doing things but it works, functions as the main function of the program running all the other functions of the program.
        """

        sys.stderr.write("\x1b[2J\x1b[h") #Clears the terminal window of content before running the program

        print("Loading Users configuration")
        self.config = config
        
        self.data = PyPWA.data.KvData.KvData(self.config["data"])
        self.calc = PyPWA.processing.DataCalc.DataCalc(self.config["calc"])

        print("Passing users data to calc object")
        self.calc.parameters = self.config["general"]["Minuit Parameters"]
        self.data.config["Use QFactor"] = self.config["general"]["Use QFactor"]
        self.calc.config["Number of Threads"] = self.config["general"]["Number of Threads"]

        print("Begining Parseing")
        self.__parser()
        print("Begining Calculation")
        self.__minimalization()

        
      

    def __parser(self):
        """
        This parses all the events into an variable, all actual parsing is done in the defined class
        """
        print("Loading events for processing.")
        self.data.parse("data")
        self.calc.kvar_data = self.data.values
        self.data.parse("accepted")
        self.calc.kvar_accepted = self.data.values
        self.data.parse("qfactor")
        if len(self.calc.kvar_data) == len(self.data.values):
            self.calc.qfactor = self.data.values
        else:
            #raise RuntimeWarning("QFactor is not the same lengh as kvar data")
            self.calc.qfactor = 1
    
    def __minimalization(self):
        """
        Minimalization function. Uses Minuit to caculate the minimal for the given function as defined by FnUser
        """
        self.calc.prep_work()
        self.minimal = iminuit.Minuit(self.calc.run, forced_parameters=self.config["general"]["Minuit Parameters"], **self.config["general"]["Initial Minuit Settings"])
        self.minimal.set_strategy(self.config["general"]["Minuit Strategy"])
        self.minimal.set_up(self.config["general"]["Minuit Set Up"])
        self.minimal.migrad(ncall=self.config["general"]["Minuit ncall"])
