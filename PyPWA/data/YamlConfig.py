#!/usr/bin/env python

"""
YamlConfig.py: This file handles all configuration in the General Shell
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "[CURRENT_VERSION]"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "[CURRENT_STATUS]"

import yaml, os

class YamlConfig(object):
    """
    Handles the processing of the configuration for PyPWA
    """

    #There are two arrays, they exist as two arrayes purely for output formatting through yaml
    default1 = {
        "calc" : {
            "Generated Length" : 10000,
            "Function Location" : "Example.py",
            "Function Name" : "the_function"
            },

        "data" : {
            "Kinematic Variable File" : "kvVars.txt",
            "Accepted Kinematic Variable File": "kvArgs.txt",
            "QFactor List Location" : "Qfactor.txt", 
            "Use Cache": True
            }
    }
    default2 = {
        "general": {
            "Initial Minuit Settings" : {'A1': 1,'A2':2,'A3':0.1,'A4':-10,'A5':-0.00001, "limit_A1": [0, 2500] },
            "Minuit Parameters" : ["A1","A2","A3","A4", "A5"],
            "Minuit Strategy" : 1,
            "Number of Threads" : 1,
            "Use QFactor" : True,
            "Minuit Set Up": 0.5,
            "Minuit ncall" : 1000
            }
        }


    python_example = "import numpy\n\n    def the_function(the_array, the_params):\n        values = numpy.zeros(shape=(len(the_array.values()[0])))\n        for x in range(len(values)):\n            values[x] = the_array[\"kvar\"][x] * the_params[\"A3\"]\n        return values\n"

    def __init__(self):
        """
        Sets up the defaults of the default settings for configuration
        """
        self.defaults = self.default1.copy()
        self.defaults.update(self.default2)

        self.the_config = self.defaults


    def generate_config(self, file_location):
        """
        Calls the loading function, the updates the internal arrays with the parsed configurations.

        Args: file_location, the location of the file you want to parse
        """
        if not os.path.isfile(file_location):
            raise IOError("{0} does not exist!".format(file_location,))

        with open(file_location) as stream:
            self.parsed_config = yaml.load(stream)

        self.the_config = self.defaults.copy()
        self.the_config.update(self.parsed_config)

    def dump_default(self, cwd):
        """
        Exports the examples using the configs and python_example.
        
        Args: cwd, the directory you want to write the examples too.
        """
        with open (cwd + "/Example.yml", "w") as stream:
            stream.write( yaml.dump(self.default1, default_flow_style=False) )
            stream.write( yaml.dump(self.default2) )
        with open (cwd + "/Example.py", "w") as stream:
            stream.write( self.python_example)
