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
        self.amplitude = amplitude
        self.setup_function = setup_function
        self.events = events
        self.parameters = parameters

    def run(self):
        self.random_setup()
        self.intensities()
        self.weighting()
        self.rejection_list
        return self.rejection

    def random_setup(self):
        self.true_random = random.SystemRandom(time.gmtime())

    def random_number(self):
        return self.true_random.random()

    def intensities(self):
        self.setup_function()
        self.intensities_list = self.amplitude(self.events, self.parameters)
        self.max_intensity = self.intensities_list.max()

    def weighting(self):
        self.weighted_list = self.intensities_list / self.max_intensity

    def rejection_list(self):
        self.rejection = numpy.zeros(shape=len(self.weighted_list), dtype=bool)
        for index, event in enumerate(weighted_list):
            if event > self.random_number():
                self.rejection[index] = True