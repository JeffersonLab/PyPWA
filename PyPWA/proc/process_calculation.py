"""
Actual process objects are defined here
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

from abc import ABCMeta, abstractmethod
import multiprocessing
import numpy
import warnings


class AbstractProcess(multiprocessing.Process):
    """Abstract class extending multiprocessing.Process
    Attributes:
        _looping  Defines if if to continue _looping, is set to true
        daemon   If process is bool, is set to true.
    """
    __metaclass__ = ABCMeta

    _looping = True
    daemon = True

    def __init__(self):
        super(AbstractProcess, self).__init__()

    def run(self):
        """Main loop for Processes"""
        self.setup()
        while self._looping:
            try:
                self.processing()
            except KeyboardInterrupt:
                return 0
        return 0

    @abstractmethod
    def setup(self):
        """Initial setup for processes"""
        pass

    @abstractmethod
    def processing(self):
        """Actual function for processing"""
        pass


class RejectionAcceptanceAmplitude(AbstractProcess):
    """Acceptance Rejection Process
    Args:
        amplitude_function (function): Users amplitude function
        setup_function (function): Setup function
        data (dict): Dictionary of numpy arrays
        parameters (dict): Parameters used to calculate
        send (Pipe): Pipe to use to send data back to the main thread
        the_id (int): id of the thread
    """

    def __init__(self, amplitude_function, setup_function, data, parameters, send, the_id):
        super(RejectionAcceptanceAmplitude, self).__init__()
        self._amplitude_function = amplitude_function
        self._setup_function = setup_function
        self._data = data
        self._parameters = parameters
        self._send = send
        self._id = the_id
        warnings.warn("RejectionAcceptanceAmplitude is being depreciated, use LoopingIntensity instead",
                      DeprecationWarning)

    def setup(self):
        """Runs the setup function"""
        self._setup_function()

    def _pipe_send(self, data):
        """Sends the data back to the main thread"""
        self._send.send(data)

    def processing(self):
        """Processes data"""
        self._pipe_send([self._id, self._amplitude_function(self._data, self._parameters)])
        self._looping = False


class LoopingIntensity(AbstractProcess):

    def __init__(self, amplitude_function, setup_function, data, send, receive, the_id=None):
        super(LoopingIntensity).__init__()
        self.amplitude = amplitude_function
        self.setup_function = setup_function
        self.data = data
        self.send = send
        self.receive = receive
        if isinstance(the_id, int):
            self.the_id = the_id
            self.tracked = True
        else:
            self.tracked = False

    def _pipe_send(self, data):
        self.send.send(data)

    def _pipe_recv(self):
        return self.receive.recv()

    def setup(self):
        self.setup_function()

    def processing(self):
        received = self._pipe_recv()
        if received == "DIE":
            self._looping = False
        else:
            intensity = self.amplitude(self.data, received)
            if self.tracked:
                values = [self.the_id, intensity]
            else:
                values = intensity
            self._pipe_send(values)


class AbstractLikelihoodAmplitude(AbstractProcess):
    """Abstract Likelihood that handles all the processing except the likelihood
    Attributes:
        setup_function (function): the function to run before calculation
        send (multiprocessing.Pipe): The pipe to send information back with
        receive (multiprocessing.Pipe): The pipe to receive parameters back from
    """

    def __init__(self, setup_function, send, receive):
        super(AbstractLikelihoodAmplitude, self).__init__()
        self._setup_function = setup_function
        self._send = send
        self._receive = receive

    def setup(self):
        """Runs the setup function"""
        self._setup_function()

    def _pipe_send(self, data):
        """Handles sending data over pipe"""
        self._send.send(data)

    def _pipe_receive(self):
        """Handles receiving data from pipe"""
        return self._receive.recv()

    def processing(self):
        """Processes the data"""
        parameters = self._pipe_receive()
        if parameters == "DIE":
            self._looping = False
        else:
            result = self.likelihood(parameters)
            self._pipe_send(result)

    @abstractmethod
    def likelihood(self, parameters):
        pass


class ExtendedLikelihoodAmplitude(AbstractLikelihoodAmplitude):
    """Likelihood Estimation Process
    Args:
        amplitude_function (function): Users amplitude function
        setup_function (function): Setup function
        processed (float): Constant for likelihood, 1/Generated_length
        data (dict): Dictionary of numpy arrays
        accepted (dict): Dictionary of numpy arrays with Accepted Monte Carlo
        send (Pipe): Pipe to use to send data back to the main thread
        receive (Pipe): Pipe to receive parameters with
    """

    def __init__(self, amplitude_function, setup_function, processed, data, accepted, send, receive):
        super(ExtendedLikelihoodAmplitude, self).__init__(setup_function, send, receive)
        self._amplitude_function = amplitude_function
        self._processed = processed
        self._data = data
        self._accepted = accepted

    def likelihood(self, parameters):
        """Calculates the likelihood function
        Args:
            parameters (dict): dictionary of the arguments to be sent to the function
        """
        processed_data = self._amplitude_function(self._data["data"], parameters)
        processed_accepted = self._amplitude_function(self._accepted["data"], parameters)
        return -(numpy.sum(self._data["QFactor"] * self._data["BinN"] * numpy.log(processed_data))) + \
                (self._processed * numpy.sum(self._accepted["BinN"] * processed_accepted))


class UnextendedLikelihoodAmplitude(AbstractLikelihoodAmplitude):
    """Likelihood Estimation Process
    Args:
        amplitude_function (function): Users amplitude function
        setup_function (function): Setup function
        data (dict): Dictionary of numpy arrays
        send (Pipe): Pipe to use to send data back to the main thread
        receive (Pipe): Pipe to receive parameters with
    """

    def __init__(self, amplitude_function, setup_function, data, send, receive):
        super(UnextendedLikelihoodAmplitude, self).__init__(setup_function, send, receive)
        self._amplitude_function = amplitude_function
        self._data = data

    def likelihood(self, parameters):
        """Calculates the likelihood function
        Args:
            parameters (dict): dictionary of the arguments to be sent to the function
        """
        processed_data = self._amplitude_function(self._data["data"], parameters)
        return -(numpy.sum(self._data["QFactor"] * self._data["BinN"] * numpy.log(processed_data)))


class ChiSquared(AbstractLikelihoodAmplitude):

    def __init__(self, amplitude_function, setup_function, data, send, receive):
        super(ChiSquared, self).__init__(setup_function, send, receive)
        self._amplitude_function = amplitude_function
        self._data = data

    def likelihood(self, parameters):
        processed_data = self._amplitude_function(self._data["data"], parameters)
        chi = numpy.float64(0.0)
        for index in range(len(processed_data)):
            if self._data["BinN"][index] == 0:
                pass
            else:
                chi += ((processed_data[index] - self._data["BinN"][index])**2) / self._data["BinN"][index]
        return chi
