#!/usr/bin/env python

"""
handlers: This file handles all configuration in the General Shell
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "[CURRENT_VERSION]"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "[CURRENT_STATUS]"

import os, warnings, yaml
from abc import ABCMeta, abstractmethod

class configurations:
    __metaclass__ = ABCMeta

    saved = None

    @abstractmethod
    def generate(self, file_location):
        pass

    @abstractmethod
    def write(self, file_location):
        pass

    def file_exists(self, file_location):
        if not os.path.isfile(file_location):
            raise IOError("{0} does not exist!".format(file_location))

class YAML(configurations):

    default_flow_style = False

    def generate(self, file_location):
        self.file_exists(file_location)

        with open(file_location) as stream:
            self.saved = yaml.load(stream)
        return self.saved

    def write(self, data, file_location):
        if  type(self.default_flow_style) != bool:
            warnings.warn("Default flow style is not boolean. Defaulting to false.", UserWarning)
            self.default_flow_style = False

        with open(file_location, "w") as stream:
            stream.write( yaml.dump(data, default_flow_style = self.default_flow_style ) )



