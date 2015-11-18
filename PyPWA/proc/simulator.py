"""
GeneralFitting.py: The GeneralShell, provides users a flexible way of testing their calcutions
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Alpha"

import time, random

class Simulator(object):

    def __init__(amplitude, events, parameters ):
        self.amplitude = amplitude
        self.parameters = parameters
        self.events = events

    def run(self):
        true_Random = random.SystemRandom(time.gmtime())

        intensities_list = self.amplitude(self.events, self.parameters)

        max_intensity = intensities_list.max()
        weighted_list = intensities_list/max_intensity
        weight = numpy.zeros(shape=(len(weighted_list)), dtype=bool)
        for event in range(len(weighted_list)):
            if weighted_list[event] > true_Random.random():
                weight[event] = True
        
        return weight