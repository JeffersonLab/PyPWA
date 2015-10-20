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
                self.settings = config["Minuit's Initial Settings"]
            except KeyError:
                pass

            try:
                self.strategy = config["Minuit's Strategy"]
            except KeyError:
                pass

            try:
                self.set_up = config["Minuit's Set Up"]
            except KeyError:
                pass

            try:
                self.ncall = config["Minuit's ncall"]
            except KeyError:
                pass


    def test(self):
        if type(self.parameters) != list:
            raise TypeError("Parameters not defined as list!")
        if type(self.settings) != dict:
            raise TypeError("Minuit settings are not a dictionary!")
        if type(self.strategy) != int:
            warnings.warn("Minuit strategy is not an integer! Defaulting to 1", UserWarning)
            self.strategy = 1
        elif not self.strategy >= 0 or not self.strategy <= 2:
            warnings.warn("Minuit's strategy must be 0, 1, or 2! Defaulting to 1", UserWarning)
            self.strategy = 1
        if type(self.ncall) != int:
            warnings.warn("ncall must be an integer! Defaulting to 1000.", UserWarning)
            self.ncall = 1000
        elif self.ncall <= 0:
            warnings.warn("ncall must be a positive integer! Defaulting to 1000", UserWarning)
            self.ncall = 1000
        if type(self.set_up) != float:
            warnings.warn("Set up must be a float! Defaulting to .5", UserWarning)
            self.set_up = float(0.5)
        

    def min(self):
        self.test()
        self.minimal = iminuit.Minuit(self.calc_function, forced_parameters=self.parameters, **self.settings )
        self.minimal.set_strategy(self.strategy)
        self.minimal.set_up(self.set_up)
        self.minimal.migrad(ncall=self.ncall)



