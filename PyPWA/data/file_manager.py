"""
PyPWA.lib.data:
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import PyPWA.data.memory_wrapper, PyPWA.data.data_tools

class MemoryInterface(object):

    def __init__(self, Cache = False, UseNew = False):
        self.Cache = Cache
        self.UseNew = UseNew

    def parse(self, file_location):
        tester = PyPWA.data.data_tools.DataTypeSearch()
        data_type = tester.search(file_location)

        if data_type == "Kv":
            reader = PyPWA.data.memory_wrapper.Kv()
            return reader.parse(file_location)
        elif data_type == "Qf":
            reader = PyPWA.data.memory_wrapper.QFactor()
            return reader.parse(file_location)
        elif data_type == "Yaml":
            reader = PyPWA.data.memory_wrapper.Yaml()
            return reader.parse(file_location)
        elif data_type == "KvCsv":
            self.UseNew = True
            reader = PyPWA.data.memory_wrapper.KvCsv()
            return reader.parse(file_location)
        elif data_type == "KvTsv":
            raise NotImplemented("TSV support is coming, but isn't done yet")
        elif data_type == "OldWeights":
            reader = PyPWA.data.memory_wrapper.OldWeights()
            return reader.parse(file_location)
        elif data_type == "NewWeights":
            self.UseNew = True
            reader = PyPWA.data.memory_wrapper.NewWeights()
            return reader.parse(file_location)


    def write(self, file_location, the_data):
        tester = PyPWA.data.data_tools.DataTypeWrite()
        data_type = tester.search(the_data, self.UseNew)

        if data_type == "Kv":
            reader = PyPWA.data.memory_wrapper.Kv()
            return reader.write(file_location, the_data)
        elif data_type == "Qf":
            reader = PyPWA.data.memory_wrapper.QFactor()
            return reader.write(file_location, the_data)
        elif data_type == "Yaml":
            reader = PyPWA.data.memory_wrapper.Yaml()
            return reader.write(file_location, the_data)
        elif data_type == "KvCsv":
            self.UseNew = True
            reader = PyPWA.data.memory_wrapper.KvCsv()
            return reader.write(file_location, the_data)
        elif data_type == "KvTsv":
            raise NotImplemented("TSV support is coming, but isn't done yet")
        elif data_type == "OldWeights":
            reader = PyPWA.data.memory_wrapper.OldWeights()
            return reader.write(file_location, the_data)
        elif data_type == "NewWeights":
            self.UseNew = True
            reader = PyPWA.data.memory_wrapper.NewWeights()
            return reader.write(file_location, the_data)

