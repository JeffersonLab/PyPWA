"""
PyPWA.lib.data:
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "[CURRENT_VERSION]"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "[CURRENT_STATUS]"

import PyPWA.data.memorywrappers, os

class MemoryInterface(object):

    supported_file_types = { 
    ".kv" : "Kv",
    ".qf" : "Qf",
    ".txt" : "Kv",
    ".yml" : "Yaml",
    ".gamp" : "Gamp",
    ".csv"  : "KvCsv",
    ".wght" : "Weights" 
    }

    cache = True

    def __init__(self, Cache = False):
        self.Cache = Cache


    def extension_test(self, file_location ):
        try:
            wrapper = self.supported_file_types[os.path.splitext(file_location)[1]]
        except KeyError:
            raise TypeError("{0} is not a supported file extension".format(os.path.splitext(file_location)[1]))

        return handlers

    def parse(self, file_location, data_type = None):
        if type(data_type) == type(None):
            wrappers = self.extension_test(file_location)
        else:
            wrappers = data_type

        if wrappers == "Kv":
            try:
                wrapper = PyPWA.data.memorywrappers.Kv()
                return wrapper.parse(file_location)
            except:
                wrapper = PyPWA.data.memorywrappers.QFactor()
                return wrapper.parse(file_location)
        elif wrappers == "Yaml":
            wrapper = PyPWA.data.memorywrappers.Yaml()
            return wrapper.parse(file_location)
        elif wrappers == "Qf":
            wrapper = PyPWA.data.memorywrappers.QFactor()
            return wrapper.parse(file_location)
        elif wrappers == "KvCsv":
            wrapper = PyPWA.data.memorywrappers.KvCsv()
            return wrapper.parse(file_location)
        elif wrappers == "Weights":
            wrapper = PyPWA.data.memorywrappers.Weights()
            return wrapper.parse(file_location)

    def write(self, file_location, the_data, data_type = None):
        if type(data_type) == type(None):
            wrappers = self.extension_test(file_location)
        else:
            wrappers = data_type

        if wrappers == "Kv":
            wrapper = PyPWA.data.memorywrappers.Kv()
            wrapper.write(file_location, data=the_data)
        elif wrappers == "Yaml":
            wrapper = PyPWA.data.memorywrappers.Yaml()
            wrapper.write(file_location, data=the_data)



