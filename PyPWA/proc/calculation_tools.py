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
        self._calc_function = calc_function
        self._parameters = parameters
        self._settings = settings
        self._strategy = strategy
        self._set_up = set_up
        self._ncall = ncall
        
    def min(self):
        minimal = iminuit.Minuit(self._calc_function, forced_parameters=self._parameters, **self._settings )
        minimal.set_strategy(self._strategy)
        minimal.set_up(self._set_up)
        minimal.migrad(ncall=self._ncall)



class FunctionLoading(object):
    def __init__(self, cwd, function_location, function_name, setup_name ):

        self._users_amplitude, self._users_setup = self._import_function(cwd, function_location, function_name, setup_name)


    def _import_function(self, cwd, function_location, function_name, setup_name):
        sys.path.append(cwd)
        try:
            imported = __import__(function_location.strip(".py"))
        except ImportError:
            raise 

        try:
            users_amplitude = getattr(imported, function_name)
        except:
            raise

        try:
            setup_function = getattr(imported, setup_name)
        except AttributeError:
            warnings.warn("Setup fucntion {0} was not found in {1}, going without setup function".format(setup_function, function_location ), UserWarning)
            def empty(): pass
            setup_function = empty

        return [ users_amplitude, setup_function ]

    def return_amplitude(self):
        return self._users_amplitude

    def return_setup(self):
        return self._users_setup



class DataSplitter(object):

    def split(self, data, num_chunks):
        if num_chunks == 1:
            return [data]

        if type(data) == dict:
            return self._dictionary_split(data, num_chunks)
        elif type(data) == numpy.ndarray:
            return self._array_split(data, num_chunks)

        return self._split_data


    def _dictionary_split(self, dictionary, num_chunks):
        split_dictionary = []
        
        for x in range(num_chunks):
            split_dictionary.append({})

        for key in dictionary:
            for index in range(num_chunks):
                split_dictionary[index][key] = numpy.array_split(dictionary[key],(num_chunks))[index]
        return split_dictionary


    def _array_split(self, array, num_chunks):
        return numpy.array_split(array, num_chunks)