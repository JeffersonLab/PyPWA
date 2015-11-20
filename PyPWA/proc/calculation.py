#!/usr/bin/env python
"""
DataCalc.py: This Caculates the from the General Shell using NumExpr
"""
from __future__ import print_function

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond", "Will Phelps", "Stephanie Bramlett"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import numpy, PyPWA.proc.tools
from abc import ABCMeta, abstractclass

class AbstractCaculation:
    __metaclass__ = ABCMeta

    @abstractclass
    def run(self): pass

class MaximalLogLikelihood(object):
    """
    This is the object used to calculate data in the arrays for the General Shell using Numexpr
    """
    
    def __init__(self, num_threads, generated_length, users_function, data, accepted, parameters, qfactor ):
        """
        Sets up basic config and checks it for errors
        """
        self.num_threads = num_threads
        self.generated_length = generated_length
        self.users_function = users_function
        self.data = data
        self.accepted = accepted
        self.parameters = parameters
        self.qfactor = qfactor

        
    def run(self, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the users function
        Params: 
        Returns: The final value from the likelihood function
        """
        
        the_params = {}
        for parameter, arg in zip(self.parameters, args):
            the_params[parameter] = arg

        for pipe in self.sendThread:
            pipe.send(the_params)
        values = numpy.zeros(shape=self.num_threads)
        for count,pipe in enumerate(self.recieveThread):
            values[count] = pipe.recv()
        value = numpy.sum(values)
        print(value)
        return value


    def prep_work(self):
        """
        Handles some initial work before processesing.
        """

        #Take care of some constants
        self.processed = (1.0/float(self.generated_length))


import time, random, numpy

class AcceptanceRejctionMethod(object):

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