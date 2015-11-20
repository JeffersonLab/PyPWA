from abc, import ABCMeta, abstractmethod
import multiprocessing, numpy

class AbstractProcess(multiprocessing.Process):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(multiprocessing.Process, self).__init__()
        self._looping = True
        self.daemon = True

    def run(self):
        self.setup()
        while self._looping:
            self.processing()
        return 0

    @abstractmethod
    def setup(self): pass

    @abstractmethod
    def processing(self): pass



class RejctionAcceptanceAmplitude(AbstractProcess):

    def __init__(self, amplitude_function, setup_function, data, parameters, send, the_id ):
        super(AbstractAmplitude, self).__init__()
        self._amplitude_function = amplitude_function
        self._setup_function = setup_function
        self._data = data
        self._parameters = parameters
        self._send = send
        self._id = the_id

    def setup(self):
        self._setup_function()

    def _pipe_send(self, data):
        self._send.send(data)

    def processing(self):
         self._pipe_send([ self._id, self._amplitude_function(self.data, self.parameters)])
         self._looping = False



class LikelihoodAmplitude(AbstractProcess):
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
        self._setup_function()

    def _pipe_send(self, data):
        self._send(data)

    def _pipe_recieve(self):
        return self._recieve.recv()

    def processing(self):
        parameters = self._pipe_recieve()
        if parameters == "DIE":
            self._looping = False
        else:
            result = self._likelihood(parameters)
            self._pipe_send(result)

    def _likelihood(self, parameters):
        processed_data = self.amplitude_function( self.data, parameters )
        processed_accepted = self.amplitude_function( self.accepted, parameters )
        return -(numpy.sum(self.qfactor * numpy.log(processed_data))) + processed * numpy.sum(processed_accepted)
