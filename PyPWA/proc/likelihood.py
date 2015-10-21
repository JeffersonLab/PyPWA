#!/usr/bin/env python
"""
DataCalc.py: This Caculates the from the General Shell using NumExpr
"""

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
    
    def __init__(self, config=None ):
        """
        Sets up basic config and checks it for errors
        """
        self.config = config

        
    def run(self, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the users function
        Params: 
        Returns: The final value from the likelihood function
        """
        
        the_params = {}
        for parameter, arg in zip(self.parameters, args):
            the_params[parameter] = arg

        if self.general["Number of Threads"] > 1:
            for pipe in self.sendThread:
                pipe.send(the_params)
            values = numpy.zeros(shape=self.general["Number of Threads"])
            for count,pipe in enumerate(self.recieveThread):
                values[count] = pipe.recv()
            value = numpy.sum(values)
            print value
            return value

        else:
            users_function = getattr(self.imported, self.config["Processing Name"])
            value = likelihood(users_function, the_params, None , self.accepted, self.data, self.processed, self.qfactor, single=True )
            print value
            return value

    def prep_work(self):
        """
        Handles some initial work before processesing.
        """

        #import and the prep and user function, then run the prep function.
        sys.path.append(self.general["cwd"])
        self.imported = __import__(self.config["Function's Location"].strip(".py"))
        prep_function = getattr(self.imported, self.config["Setup Name"])
        users_function = getattr(self.imported, self.config["Processing Name"])
        prep_function()


        #Split the arrays up if there is more than one thread
        if self.general["Number of Threads"] > 1:
            self.data_split = []
            self.accepted_split = []
            
            for x in range((self.general["Number of Threads"])):
                self.data_split.append({})
                self.accepted_split.append({})

            for key in self.data:
                for x in range((self.general["Number of Threads"])):
                    self.data_split[x][key] = numpy.array_split(self.data[key],(self.general["Number of Threads"]))[x]

            for key in self.accepted:
                for x in range((self.general["Number of Threads"])):
                    self.accepted_split[x][key] = numpy.array_split(self.accepted[key], (self.general["Number of Threads"]))[x]

            if isinstance(self.qfactor, numpy.ndarray):
                self.qfactor_split = numpy.array_split(self.qfactor, (self.general["Number of Threads"]))
            else:
                self.qfactor_split = numpy.array_split(numpy.ones(shape=len(self.data.values()[0]), dtype="float64"), (self.general["Number of Threads"]))
        else:

            if not isinstance(self.qfactor, numpy.ndarray):
                self.qfactor = numpy.ones(shape=len(self.data.values()[0]))

        #Take care of some constants
        self.processed = (1.0/float(self.config["Generated Length"]))

        #Assign threads if there are more than one thread

        if self.general["Number of Threads"] > 1:

            self.sendMain = []
            self.recieveMain = []
            self.sendThread = []
            self.recieveThread = []
            self.processes = []

            for x in range(self.general["Number of Threads"]):
                recieve, send = multiprocessing.Pipe(False)
                self.sendThread.append(send)
                self.recieveMain.append(recieve)
            for x in range(self.general["Number of Threads"]):
                recieve, send = multiprocessing.Pipe(False)
                self.sendMain.append(send)
                self.recieveThread.append(recieve)

            for count, pipe in enumerate(zip(self.sendMain, self.recieveMain)):
                self.processes.append(multiprocessing.Process(target=likelihood, args=(users_function, pipe[0],pipe[1], self.accepted_split[count], self.data_split[count], self.processed, self.qfactor_split[count])))
            for process in self.processes:
                process.daemon = True
            for process in self.processes:
                process.start()

    def stop(self):
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


