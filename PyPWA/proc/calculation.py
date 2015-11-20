#!/usr/bin/env python
"""
DataCalc.py: This Caculates the from the General Shell using NumExpr
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond", "Will Phelps", "Stephanie Bramlett"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import numpy, time, random
import PyPWA.proc.calculation_tools, PyPWA.proc.process_calulation, PyPWA.proc.process_communication
from abc import ABCMeta, abstractclass

class InterfaceCalculation:
    __metaclass__ = ABCMeta

    @abstractclass
    def run(self): pass



class MaximalLogLikelihood(InterfaceCalculation):
    """
    This is the object used to calculate data in the arrays for the General Shell using Numexpr
    """
    
    def __init__(self, num_threads, parameters, data, accepted, qfactor, generated_length, amplitude_function, setup_function ):
        self._num_threads = num_threads
        self._parameters = parameters
        self._send_to_process, recieve_from_main, send_to_main, self._recieve_from_process = self._pipe_setup()

        split_data, split_accepted, split_qfactor = _data_setup(data, accepted, qfactor )
        processed = _preprocessed(generated_length)

        self._thread_setup( amplitude_function, setup_function, processed, split_data, split_accepted, split_qfactor, send_to_main, recieve_from_main)


    def _data_setup(self, data, accepted, qfactor ):
        splitter = PyPWA.proc.calculation_tools.DataSplitter()
        split_data = splitter.split(data, self.num_threads)
        split_accepted = splitter.split(accepted, self.num_threads)
        split_qfactor = splitter.split(qfactor, self.num_threads)
        return [split_data, split_accepted, split_qfactor]


    def _pipe_setup(self):
        pipe_communication = PyPWA.proc.process_communication.ProcessPipes()

        send_to_process, recieve_from_main = pipe_communication.return_pipes(self.num_threads)
        send_to_main, recieve_from_process = pipe_communication.return_pipes(self.num_threads)

        return [send_to_process, recieve_from_main, send_to_main, recieve_from_process ]


    def _preprocessed(self, generated_length):
        """
        Handles some initial work before processesing.
        """
        return (1.0/float(generated_length))


    def _thread_setup(self, amplitude_function, setup_function, processed, data, accepted, qfactor, send_to_main, recieve_from_main ):

        processes = []

        for count, pipe in enumerate(zip(send_to_main, recieve_from_main)):
                processes.append(PyPWA.proc.process_calulation.LikelihoodAmplitude(amplitude_function, setup_function, processed, data[count], accepted[counnt], qfactor[count], send[0], recieve[1]))

        for process in processes:
            process.start()

        
    def run(self, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the users function
        Params: 
        Returns: The final value from the likelihood function
        """
        
        parameters_with_values = {}
        for parameter, arg in zip(self._parameters, args):
            parameters_with_values[parameter] = arg

        for pipe in self._send_to_process:
            pipe.send(parameters_with_values)

        values = numpy.zeros(shape=self._num_threads)

        for index, pipe in enumerate(self._recieve_from_process):
            values[index] = pipe.recv()

        final_value = numpy.sum(values)
        print(final_value)
        return final_value


    def stop(self):
        for pipe in self._send_to_process:
            pipe.send("DIE")



class AcceptanceRejctionMethod(InterfaceCalculation):

    def __init__(self, num_threads, events, amplitude_function, setup_function, parameters ):
        self._num_threads = num_threads
        self.random = self._random_setup()
        split_events = self._data_setup(events)
        send_to_main, self._recieve_from_process = self._pipe_setup()
        self.processes = self._thread_setup( amplitude_function, setup_function, split_events, parameters, send_to_main )


    def _random_setup(self):
        return random.SystemRandom(time.gmtime())


    def _data_setup(self, data, num_threads):
        splitter = PyPWA.proc.calculation_tools.DataSplitter()
        return splitter.split(data, num_threads)


    def _pipe_setup(self):
        pipe_communication = PyPWA.proc.process_communication.ProcessPipes()
        send_to_main, recieve_from_process = pipe_communication.return_pipes(self.num_threads)
        return [send_to_main, recieve_from_process]


    def _thread_setup(self, amplitude_function, setup_function, split_events, parameters, send_to_main):
        processes = []

        for index, pipe in enumerate(send_to_main):
                processes.append(PyPWA.proc.process_calulation.RejctionAcceptanceAmplitude(amplitude_function, setup_function, split_events[index], parameters, send, index))

        return processes


    def run(self):
        intensities_list, max_intensity = self._intensities()
        weight_list =  self._weighting(intensities_list, max_intensity)
        rejection_list = self._rejection_list(weight_list)
        return rejection_list


    def _intensities(self):
        results = []

        for count in range(self.num_threads):
            results.append(0)

        for process in self.processes:
            process.start()

        for pipe in self._recieve_from_process:
            result = pipe.recv()
            results[result[0]] = result[1]

        intensities_list = numpy.concatenate(results)
        max_intensity = intensities_list.max()

        return [intensities_list, max_intensity]


    def _weighting(self, intensities, max_intensity):
        return intensities_list / max_intensity


    def _rejection_list(self, weighted_list):
        rejection = numpy.zeros(shape=len(weighted_list), dtype=bool)
        for index, event in enumerate(weighted_list):
            if event > self._random.random():
                rejection[index] = True
        return rejection