"""
tools.py: Tools needed for the various Amplitude analysing utilities.
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import iminuit, warnings, sys, numpy

class Minimalizer(object):


    def __init__(self, calc_function, parameters, settings, strategy, set_up, ncall):
        self.calc_function = calc_function
        self.parameters = parameters
        self.settings = settings
        self.strategy = strategy
        self.set_up = set_up
        self.ncall = ncall
        

    def min(self):
        self.minimal = iminuit.Minuit(self.calc_function, forced_parameters=self.parameters, **self.settings )
        self.minimal.set_strategy(self.strategy)
        self.minimal.set_up(self.set_up)
        self.minimal.migrad(ncall=self.ncall)

class FunctionLoading(object):
    def __init__(self, cwd, function_location, function_name, setup_name = None ):
        self.cwd = cwd
        self.function_location = function_location
        self.function_name = function_name
        self.setup_name = setup_name

        self.__import_function()

    def _import_function(self):
        sys.path.append(self.cwd)
        try:
            imported = __import__(self.function_location.strip(".py"))
        except ImportError:
            raise 

        try:
            self.users_function = getattr(imported, self.function_name)
        except AttributeError:
            raise ValueError("There is not function named {0} in the function file!".format(self.function_name))

        try:
            self.setup_function = getattr(imported, self.setup_name)
        except AttributeError:
            warnings.warn("Setup fucntion {0} was not found in {1}, going without setup function".format(self.setup_function, self.function_location ), UserWarning)
            self.setup_function = empty_function

    @staticmethod
    def empty_function():
        pass

    def return_amplitude(self):
        return self.users_function

    def return_setup(self):
        return self.setup_function

class DataChunking(object):

    _num_chunks = 0
    _data = None
    _split_data = None

    def chunks(self, data, num_chunks):
        if num_chunks == 1:
            return [data]

        self._num_chunks = num_chunks
        self._data = data

        if type(self._data) == dict:
            self._dictionary_split()
        elif type(self._data) == numpy.ndaray:
            self._array_split()

        return self._split_data


    def _dictionary_split(self):
        self._split.data = []
        
        for x in range(self._num_chunks):
            self._split_data.append({})

        for key in self._data:
            for index in range(self._num_chunks):
                self._split_data[index][key] = numpy.array_split(self._data[key],(self._num_chunks))[index]


    def _array_split(self):
        self._split_data = numpy.array_split(self._data, self._num_chunks)