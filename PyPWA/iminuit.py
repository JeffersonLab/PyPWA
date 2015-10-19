"""
iminuit.py: Handles Iminuit and its parsing of data.
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__= "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__= "Alpha.1"

import iminuit, warnings, inspect

class Minimalizer(object):

    calc_function = None
    parameters = None
    settings = None
    strategy = None
    set_up = None
    ncall = None

    def __init__(self, config = None):
        if type(config) != type(None):

            try:
                self.calc_function = config["calc"]
            except KeyError:
                pass

            try:
                self.parameters = config["Minuit's Parameters"]
            except KeyError:
                pass

            try:
                self.settings = config["Minuit's Initial Setttings"]
            except KeyError:
                pass

            try:
                self.strategy = config["Minuit's Strategy"]
            except KeyError:
                pass

            try:
                self.set_up = config["Minuit's Set up"]
            except KeyError:
                pass

            try:
                self.ncall = config["Minuit's ncall"]
            except KeyError:
                pass


    def test(self):
        self.function_test( self.calc_function)
        if type(parameters) != list:
            raise TypeError("Parameters not defined as list!")
        if type(self.settings) != dict:
            raise TypeError("iMinuit settings are not a dictionary!")
        if type(self.strategy) != int:
            warnings.warn("iMinuit strategy is not an integer! Defaulting to 1", UserWarning)
            self.strategy = 1
        elif not self.strategy >= 0 or not self.strategy <= 2:
            warnings.warn("iMinuit's strategy must be 0, 1, or 2! Defaulting to 1", UserWarning)
            self.strategy = 1
        if type(self.ncall) != int:
            warnings.warn("ncall must be an integer! Defaulting to 1000.", UserWarning)
            self.ncall = 1000
        elif self.ncall <= 0:
            warnings.warn("ncall must be a positive integer! Defaulting to 1000", UserWarning)
            self.ncall = 1000


    def function_test(self, function, eow ):
        def holding_function(self):
            pass

        if hasattr(function, "__call__"):
            if inspect.getargspec( function ).args == []:
                return function
            else:
                raise TypeError("User defined function has arguments!")
        else:
            raise TypeError("User defined function is not a function!")
        

    def min(self):
        self.test()
        self.minimal = iminuit.Minuit(self.calc_function, forced_parameters=self.parameters, **self.settings )
        self.minimal.set_strategy(self.strategy)
        self.minimal.set_up(self.set_up)
        self.minimal.migrad(ncall=self.ncall)



