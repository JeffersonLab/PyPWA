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
import multiprocessing, numpy

class AbstractProcess(multiprocessing.Process):
    """Abstract class extendeding multiprocessing.Process
    Attributes:
        _looping (optional[bool]): Default True. Defines if if to continue _looping
        daemon (optional[bool]): Default True. If process is bool
    """
    __metaclass__ = ABCMeta

    _looping = True
    daemon = True

    def __init__(self):
        super(multiprocessing.Process, self).__init__()

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


class RejctionAcceptanceAmplitude(AbstractProcess):
    """Acceptance Rejection Process
    Args:
        amplitude_function (object): Users amplitude function
        setup_function (object): Setup function
        data (dict): Dictionary of numpy arrays
        parameters (dict): Parameters used to calculate
        send (Pipe): Pipe to use to send data back to the main thread
        the_id (int): id of the thread
    """

    def __init__(self, amplitude_function, setup_function, data, parameters, send, the_id ):
        super(AbstractProcess, self).__init__()
        self._amplitude_function = amplitude_function
        self._setup_function = setup_function
        self._data = data
        self._parameters = parameters
        self._send = send
        self._id = the_id


    def setup(self):
        """Runs the setup fucntion"""
        self._setup_function()


    def _pipe_send(self, data):
        """Sends the data back to the main thread"""
        self._send.send(data)


    def processing(self):
        """Processes data"""
        self._pipe_send([ self._id, self._amplitude_function(self._data, self._parameters)])
        self._looping = False


class LikelihoodAmplitude(AbstractProcess):
    """Liklihood Estimation Process
    Args:
        amplitude_function (object): Users amplitude function
        setup_function (object): Setup function
        processed (float): Constant for likelihood, 1/Generated_length
        data (dict): Dictionary of numpy arrays
        accepted (dict): Dictionary of numpy arrays with Accepted Monte Carlo
        send (Pipe): Pipe to use to send data back to the main thread
        recieve (Pipe): Pipe to receive parameters with
    """

    def __init__(self, amplitude_function, setup_function, processed, data, accepted, qfactor, send, recieve ):
        super(AbstractProcess, self).__init__()
        self._amplitude_function = amplitude_function
        self._setup_function = setup_function
        self._processed = processed
        self._data = data
        self._accepted = accepted
        self._qfactor = qfactor
        self._send = send
        self._recieve = recieve


    def setup(self):
        """Runs the setup fucntion"""
        self._setup_function()


    def _pipe_send(self, data):
        """Handles sending data over pipe"""
        self._send.send((data))


    def _pipe_recieve(self):
        """Handles recieving data from pipe"""
        return self._recieve.recv()


    def processing(self):
        """Processes the data"""
        parameters = self._pipe_recieve()
        if parameters == "DIE":
            self._looping = False
        else:
            result = self._likelihood(parameters)
            self._pipe_send(result)


    def _likelihood(self, parameters):
        """Calculates the likelihood function"""
        processed_data = self._amplitude_function( self._data, parameters )
        processed_accepted = self._amplitude_function( self._accepted, parameters )
        return -(numpy.sum(self._qfactor * numpy.log(processed_data))) + self._processed * numpy.sum(processed_accepted)
