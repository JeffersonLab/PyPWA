"""
Multiprocessing Calculation
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond", "Will Phelps", "Stephanie Bramlett"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import random
import time

import numpy
from abc import ABCMeta

from PyPWA.libs.proc import calculation_tools, process_calculation, process_communication


class SimplexCommunication(object):
    def __init__(self):
        self.something = "I do things"

    def run(self):
        return self.something


class DuplexCommunication(object):
    def __init__(self):
        self.something = "I do more things"

    def run(self):
        return self.something


class CalculationBuilder(object):
    def __init__(self, duplex):
        self.duplex = duplex


class AbstractFitting(object):
    __metaclass__ = ABCMeta

    """Object that handles the Maximum-Likelihood Estimation

    All arguments are in the order of their use inside the init method.

    Args:
        num_threads (int): Number of processes to use.
        parameter_names (list): Parameters to use in calculation
    """

    def __init__(self, num_threads, parameter_names):

        self._num_threads = num_threads
        self._parameter_names = parameter_names
        self._send_to_process, self.receive_from_main, self.send_to_main, self._receive_from_process = \
            self._pipe_setup()

    def _data_setup(self, data):
        splitter = calculation_tools.DictionarySplitter()
        split_data = splitter.split(data, self._num_threads)
        return split_data

    def _pipe_setup(self):
        pipe_communication = process_communication.ProcessPipes()

        send_to_process, receive_from_main = pipe_communication.return_pipes(self._num_threads)
        send_to_main, receive_from_process = pipe_communication.return_pipes(self._num_threads)

        return [send_to_process, receive_from_main, send_to_main, receive_from_process]

    def run(self, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the users function
        Args:
            *args: The parameters in list format
        Returns:
            float: The final value from the likelihood function
        """

        parameters_with_values = {}
        for parameter, arg in zip(self._parameter_names, args):
            parameters_with_values[parameter] = arg

        for pipe in self._send_to_process:
            pipe.send(parameters_with_values)

        values = numpy.zeros(shape=self._num_threads)

        for index, pipe in enumerate(self._receive_from_process):
            values[index] = pipe.recv()

        final_value = self.final_calc(values)
        print(final_value)
        return final_value

    def final_calc(self, values):
        return numpy.sum(values)

    def stop(self):
        """Shuts down processes"""
        for pipe in self._send_to_process:
            pipe.send("DIE")


class MaximumLogLikelihoodExtendedEstimation(AbstractFitting):
    """Object that handles the Maximum-Likelihood Estimation

    All arguments are in the order of their use inside the init method.

    Args:
        num_threads (int): Number of processes to use.
        parameter_names (list): Parameters to use in calculation
        data (dict): Dictionary of arrays with data events
        accepted (dist): Dictionary of arrays with accepted monte carlo events
        generated_length (int): Number of generated events
        amplitude_function (object): Function that calculates amplitude
        setup_function (object): Function that runs before any calculation
    """

    def __init__(self, num_threads, parameter_names, data, accepted, generated_length, amplitude_function,
                 setup_function):
        super(MaximumLogLikelihoodExtendedEstimation, self).__init__(num_threads, parameter_names)

        split_data = self._data_setup(data)
        split_accepted = self._data_setup(accepted)
        processed = self._preprocessed(generated_length)

        self._thread_setup(amplitude_function, setup_function, processed, split_data, split_accepted, self.send_to_main,
                           self.receive_from_main)

    @staticmethod
    def _preprocessed(generated_length):
        """
        Handles some initial work before processing.
        """
        return 1.0 / float(generated_length)

    @staticmethod
    def _thread_setup(amplitude_function, setup_function, processed, data, accepted, send_to_main,
                      receive_from_main):

        processes = []

        for count, pipe in enumerate(zip(send_to_main, receive_from_main)):
                processes.append(
                    process_calculation.ExtendedLikelihoodAmplitude(amplitude_function, setup_function, processed,
                                                                    data[count], accepted[count],
                                                                    pipe[0], pipe[1])
                )

        for process in processes:
            process.start()


class MaximumLogLikelihoodUnextendedEstimation(AbstractFitting):
    """Object that handles the Maximum-Likelihood Estimation

    All arguments are in the order of their use inside the init method.

    Args:
        num_threads (int): Number of processes to use.
        parameter_names (list): Parameters to use in calculation
        data (dict): Dictionary of arrays with data events
        amplitude_function (object): Function that calculates amplitude
        setup_function (object): Function that runs before any calculation
    """

    def __init__(self, num_threads, parameter_names, data, amplitude_function, setup_function):
        super(MaximumLogLikelihoodUnextendedEstimation, self).__init__(num_threads, parameter_names)
        split_data = self._data_setup(data)

        self._thread_setup(amplitude_function, setup_function, split_data, self.send_to_main, self.receive_from_main)

    @staticmethod
    def _thread_setup(amplitude_function, setup_function, data, send_to_main, receive_from_main):

        processes = []

        for count, pipe in enumerate(zip(send_to_main, receive_from_main)):
                processes.append(
                    process_calculation.UnextendedLikelihoodAmplitude(amplitude_function, setup_function, data[count],
                                                                      pipe[0], pipe[1])
                )

        for process in processes:
            process.start()


class ChiSquaredTest(AbstractFitting):
    """Object that handles the Maximum-Likelihood Estimation

    All arguments are in the order of their use inside the init method.

    Args:
        num_threads (int): Number of processes to use.
        parameter_names (list): Parameters to use in calculation
        data (dict): Dictionary of arrays with data events
        amplitude_function (function): Function that calculates amplitude
        setup_function (function): Function that runs before any calculation
    """

    def __init__(self, num_threads, parameter_names, data, amplitude_function, setup_function):
        super(ChiSquaredTest, self).__init__(num_threads, parameter_names)
        split_data = self._data_setup(data)

        self._thread_setup(amplitude_function, setup_function, split_data, self.send_to_main, self.receive_from_main)

    @staticmethod
    def _thread_setup(amplitude_function, setup_function, data, send_to_main, receive_from_main):

        processes = []

        for count, pipe in enumerate(zip(send_to_main, receive_from_main)):
                processes.append(
                    process_calculation.ChiSquared(amplitude_function, setup_function, data[count], pipe[0], pipe[1])
                )

        for process in processes:
            process.start()


class CalculateIntensities(object):
    """Main Object for Acceptance Rejection Method
    Args:
        num_threads (int): Number of processes to use.
        events (dict): Dictionary of Arrays of events
        amplitude_function (function): Function that calculates amplitude
        setup_function (function): Function that runs before any calculation
        parameters (list): Parameters to use in calculation
    """

    def __init__(self, num_threads, events, amplitude_function, setup_function, parameters):
        self._num_threads = num_threads
        split_events = self._data_setup(events)
        send_to_main, self._receive_from_process = self._pipe_setup()
        self.processes = self._thread_setup(amplitude_function, setup_function, split_events, parameters, send_to_main)

    def _data_setup(self, data):
        splitter = calculation_tools.DictionarySplitter()
        return splitter.split(data, self._num_threads)

    def _pipe_setup(self):
        """

        Returns:
            list: [send, receive]
        """
        pipe_communication = process_communication.ProcessPipes()
        send_to_main, receive_from_process = pipe_communication.return_pipes(self._num_threads)
        return [send_to_main, receive_from_process]

    @staticmethod
    def _thread_setup(amplitude_function, setup_function, split_events, parameters, send_to_main):
        processes = []

        for index, pipe in enumerate(send_to_main):
                processes.append(
                    process_calculation.RejectionAcceptanceAmplitude(amplitude_function, setup_function,
                                                                     split_events[index], parameters, pipe, index)
                )

        return processes

    def run(self):
        results = []

        for count in range(self._num_threads):
            results.append(0)

        for process in self.processes:
            process.start()

        for pipe in self._receive_from_process:
            result = pipe.recv()
            results[result[0]] = result[1]

        intensities_list = numpy.concatenate(results)
        max_intensity = intensities_list.max()

        return [intensities_list, max_intensity]


class AcceptanceRejectionMethod(object):

    def __init__(self, intensities_list, max_intensity):
        self.random = self._random_setup()
        self._intensities_list = intensities_list
        self._max_intensity = max_intensity

    @staticmethod
    def _random_setup():
        return random.SystemRandom(time.gmtime())

    def run(self):
        """Main method that starts processing"""

        weighted_list = self._intensities_list / self._max_intensity

        rejection = numpy.zeros(shape=len(weighted_list), dtype=bool)
        for index, event in enumerate(weighted_list):
            if event > self.random.random():
                rejection[index] = True
        return rejection
