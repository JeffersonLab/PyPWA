"""
Handles communication for processes
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import multiprocessing


class SingleFactory(object):
    def __init__(self, count):
        self.count = count
        self._sends = False
        self._receives = False

    def build(self, force=False):
        if not self.pipes or force:
            self._sends = [0] * self.count
            self._receives = [0] * self.count

            for pipe in range(self.count):
                receive, send = multiprocessing.Pipe(False)
                self._sends[pipe] = SingleSend(send)
                self._receives[pipe] = SingleReceive(receive)

        return self.pipes

    @property
    def pipes(self):
        return [self._sends, self._receives]


class DuplexFactory(object):
    def __init__(self, count):
        self.count = count
        self._main = False
        self._process = False

    def build(self, force=False):
        if not self._main or force:
            self._main = [0] * self.count
            self._process = [0] * self.count

            for pipe in range(self.count):
                receive_one, send_one = multiprocessing.Pipe(False)
                receive_two, send_two = multiprocessing.Pipe(False)

                self._main[pipe] = DuplexCommunication(send_one, receive_two)
                self._process[pipe] = DuplexCommunication(send_two, receive_one)

        return self.pipes

    @property
    def pipes(self):
        return [self._main, self._process]


class SingleSend(object):

    def __init__(self, send_pipe):
        self.send_pipe = send_pipe

    def send(self, ):
        self.send_pipe.send()


class SingleReceive(object):

    def __init__(self, receive_pipe):
        self.receive_pipe = receive_pipe

    def receive(self):
        return self.receive_pipe.recv()


class DuplexCommunication(object):

    def __init__(self, send_pipe, receive_pipe):
        self.send_pipe = send_pipe
        self.receive_pipe = receive_pipe

    def send(self, data):
        self.send_pipe.send(data)

    def receive(self):
        return self.receive_pipe.recv()