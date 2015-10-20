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

import numpy, multiprocessing, sys,  warnings

class Calc(object):
    """
    This is the object used to calculate data in the arrays for the General Shell using Numexpr
    """

    general = {}
    
    def __init__(self, config ):
        """
        Sets up basic config and checks it for errors
        """
        self.config = config
        self.preprocessing()


        
    def run(self, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the users function
        Params: 
        Returns: The final value from the likelihood function
        """
        
        the_params = {}
        for parameter, arg in zip(self.parameters, args):
            the_params[parameter] = arg


        users_function = getattr(self.imported, self.config["Processing Name"])

        if self.general["Number of Threads"] > 1:
            accepted_pool = multiprocessing.Pool(processes=self.general["Number of Threads"])
            data_pool = multiprocessing.Pool(processes=self.general["Number of Threads"])

            accepted_jobs = []
            for x in range((self.general["Number of Threads"])):
                accepted_jobs.append(accepted_pool.apply_async(accepted_process, args=(users_function, self.accepted_split[x],the_params, self.processed)))

            data_jobs = []
            for x in range((self.general["Number of Threads"])):
                data_jobs.append(data_pool.apply_async(data_process, args=(users_function, self.data_split[x], the_params, self.qfactor_split[x])))

            #You must close the pool before you can wait until the threads die
            data_pool.close()
            accepted_pool.close()

            try:
                accepted_pool.join()
                accepted_final = [completed.get() for completed in accepted_jobs ]
                accepted_value = numpy.sum(accepted_final)
            except KeyboardInterrupt:
                worker_pool.terminate()
                worker_pool.join()
                sys.exit()

            try:
                data_pool.join()
                data_final = [completed.get() for completed in data_jobs ]
                data_value = numpy.sum(data_final)
            except KeyboardInterrupt:
                worker_pool.terminate()
                worker_pool.join()
                sys.exit()

            value = accepted_value + data_value

        else:
            value = self.likely_hood_function( users_function(self.data, the_params), users_function(self.accepted, the_params), self.qfactor)
            print value
        return value


    def prep_work(self):
        """
        Handles some initial work before processesing.
        """

        sys.path.append(self.general["cwd"])
        self.imported = __import__(self.config["Function's Location"].strip(".py"))
        prep_function = getattr(self.imported, self.config["Setup Name"])
        prep_function()

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


    def preprocessing(self):
        """
        Processes static data for the likelihood function.
        """
        self.processed = (1.0/float(self.config["Generated Length"]))

    def likely_hood_function(self, array_data, array_accpeted, qfactor):
        """
        Returns the final likelihood function value
        """
        return -(numpy.sum(qfactor * numpy.log(array_data))) + self.processed * numpy.sum(array_accpeted)
    
def accepted_process(function, array, params, processed):
    """
    Handles the accepted half of the likelihood function
    """
    values = function(array, params)
    return processed * numpy.sum(values) 

def data_process(function, array, params, qfactor):
    """
    Handles the data half of the likelihood funciton.
    """
    values = function(array, params)
    the_values = numpy.zeros(shape=len(values), dtype="float64")
    for x in range(len(values)):
        the_values[x] = qfactor[x] * numpy.log(values[x])
    return -(numpy.sum(the_values))