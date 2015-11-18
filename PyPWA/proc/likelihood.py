#!/usr/bin/env python
"""
DataCalc.py: This Caculates the from the General Shell using NumExpr
"""
from __future__ import print_function

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond", "Will Phelps", "Stephanie Bramlett"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta"

import numpy, sys,  warnings, multiprocessing

class Calc(object):
    """
    This is the object used to calculate data in the arrays for the General Shell using Numexpr
    """

    general = {}
    
    def __init__(self, num_threads, generated_length, users_function, data, accepted, parameters ):
        """
        Sets up basic config and checks it for errors
        """
        self.num_threads = num_threads
        self.generated_length = generated_length
        self.users_function = users_function
        self.data = data
        self.accepted

        
    def run(self, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the users function
        Params: 
        Returns: The final value from the likelihood function
        """
        
        the_params = {}
        for parameter, arg in zip(self.parameters, args):
            the_params[parameter] = arg

        if self.num_threads > 1:
            for pipe in self.sendThread:
                pipe.send(the_params)
            values = numpy.zeros(shape=self.num_threads)
            for count,pipe in enumerate(self.recieveThread):
                values[count] = pipe.recv()
            value = numpy.sum(values)
            print(value)
            return value

        else:
            value = likelihood(self.users_function, the_params, None , self.accepted, self.data, self.processed, self.qfactor, single=True )
            print(value)
            return value


    def prep_work(self):
        """
        Handles some initial work before processesing.
        """

        #Split the arrays up if there is more than one thread
        if self.num_threads > 1:
            self.data_split = []
            self.accepted_split = []
            
            for x in range((self.num_threads)):
                self.data_split.append({})
                self.accepted_split.append({})

            for key in self.data:
                for x in range((self.num_threads)):
                    self.data_split[x][key] = numpy.array_split(self.data[key],(self.num_threads))[x]

            for key in self.accepted:
                for x in range((self.num_threads)):
                    self.accepted_split[x][key] = numpy.array_split(self.accepted[key], (self.num_threads))[x]

            if isinstance(self.qfactor, numpy.ndarray):
                self.qfactor_split = numpy.array_split(self.qfactor, (self.num_threads))
            else:
                self.qfactor_split = numpy.array_split(numpy.ones(shape=len(self.data.values()[0]), dtype="float64"), (self.num_threads))
        else:

            if not isinstance(self.qfactor, numpy.ndarray):
                self.qfactor = numpy.ones(shape=len(self.data.values()[0]))

        #Take care of some constants
        self.processed = (1.0/float(self.generated_length))

        #Assign threads if there are more than one thread

        if self.num_threads > 1:

            self.sendMain = []
            self.recieveMain = []
            self.sendThread = []
            self.recieveThread = []
            self.processes = []

            for x in range(self.num_threads):
                recieve, send = multiprocessing.Pipe(False)
                self.sendThread.append(send)
                self.recieveMain.append(recieve)
            for x in range(self.num_threads):
                recieve, send = multiprocessing.Pipe(False)
                self.sendMain.append(send)
                self.recieveThread.append(recieve)

            for count, pipe in enumerate(zip(self.sendMain, self.recieveMain)):
                self.processes.append(multiprocessing.Process(target=likelihood, args=(self.users_function, pipe[0],pipe[1], self.accepted_split[count], self.data_split[count], self.processed, self.qfactor_split[count])))
            for process in self.processes:
                process.daemon = True
            for process in self.processes:
                process.start()

    def stop(self):
        if self.num_threads > 1:
            for pipe in self.sendThread:
                pipe.send("DIE") 


def likelihood(users_function, send, recieve, accepted, data, processed, qfactor, single=False ):
    while True:
        if not single:
            params = recieve.recv()
        else:
            params = send
        if params == "DIE":
            return 0 
        else:
            processed_data = users_function(data, params)
            processed_accepted = users_function(accepted, params)
            value = -(numpy.sum(qfactor * numpy.log(processed_data))) + processed * numpy.sum(processed_accepted)
            if not single:
                send.send(value)
            else:
                return value