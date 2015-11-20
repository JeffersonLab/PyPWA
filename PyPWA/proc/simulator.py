"""
GeneralFitting.py: The GeneralShell, provides users a flexible way of testing their calcutions
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import time, random, numpy

class Simulator(object):

    def __init__(self, amplitude, setup_function, events, parameters ):
        self.__amplitude = amplitude
        self.__setup_function = setup_function
        self.__events = events
        self.__parameters = parameters

    def run(self):
        self.__random_setup()
        self.__intensities()
        self.__weighting()
        self.__rejection_list
        return self.__rejection

    def __random_setup(self):
        self.__true_random = random.SystemRandom(time.gmtime())

    def __random_number(self):
        return self.__true_random.random()

    def __intensities(self):
        self.__setup_function()
        self.__intensities_list = self.__amplitude(self.__events, self.__parameters)
        self.__max_intensity = self.__intensities_list.max()

    def __weighting(self):
        self.__weighted_list = self.__intensities_list / self.__max_intensity

    def __rejection_list(self):
        self.__rejection = numpy.zeros(shape=len(self.__weighted_list), dtype=bool)
        for index, event in enumerate(weighted_list):
            if event > self.__random_number():
                self.__rejection[index] = True