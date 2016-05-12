# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Handles communication for processes
"""

import multiprocessing
import logging

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class SimplexFactory(object):
    def __init__(self, count):
        """
        This object returns the requested amount of simplex pipes that can be
        used for inter-process communication.

        Args:
            count (int): The number of Simplex Processes
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self.count = count
        self._sends = False
        self._receives = False

    def build(self):
        """
        When called this method will build the pipes and nest the into the
        SingleSend and SingleReceive objects to be sent to the main process and
        sub processes alike.

        Returns:
            list [[SingleSend],[SingleReceive]]
        """

        self._sends = [0] * self.count
        self._receives = [0] * self.count

        for pipe in range(self.count):
            receive, send = multiprocessing.Pipe(False)
            self._sends[pipe] = SimplexSend(send)
            self._receives[pipe] = SimplexReceive(receive)

        return self.pipes

    @property
    def pipes(self):
        """
        Call to return the pipes.

        Returns:
            list[list[SimplexSend],list[SimplexReceive]]
        """
        return [self._sends, self._receives]


class DuplexFactory(object):
    def __init__(self, count):
        """
        This object returns the requested amount of duplex pipes that can be
        used for inter-process communication.

        Args:
            count (int): The number of Duplex Processes.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self.count = count
        self._main = False
        self._process = False

    def build(self):
        """
        When called this method will build the pipes and nest them into the
        DuplexCommunication object to be sent to the main process and sub
        processes.

        Returns:
            list [list[DuplexCommunication],list[DuplexCommunication]]
        """
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
        """
        Call to return the pipes.

        Returns:
            list[list[DuplexCommunication],list[DuplexCommunication]]
        """
        return [self._main, self._process]


class CommunicationInterface(object):

    def send(self, data):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError


class SimplexSend(CommunicationInterface):
    def __init__(self, send_pipe):
        """
        Simple Send object

        Args:
            send_pipe (multiprocessing.Pipe): The pipe that can be used to
                send data
        """
        self.send_pipe = send_pipe

    def send(self, data):
        """
        Call to send data

        Args:
            data: Any pickle-able data
        """
        self.send_pipe.send(data)

    def receive(self):
        """
        Null Call to receive method.

        Raises:
            SimplexError: Simplex object can only send data.
        """
        raise SimplexError("Communication Object is Simplex and doesn't support"
                           " the receive method.")


class SimplexReceive(CommunicationInterface):
    def __init__(self, receive_pipe):
        """
        Simple Receive object

        Args:
            receive_pipe (multiprocessing.Pipe): The pipe that can be used to
                receive data
        """
        self.receive_pipe = receive_pipe

    def send(self, data):
        """
        Null call to send method.

        Raises:
            SimplexError: Simplex object can only receive.
        """
        raise SimplexError("Communication Object is Simplex and doesn't support"
                           " the send method.")

    def receive(self):
        """
        Call to fetch data from the pipe.

        Returns:
            object: Anything that can be pickled
        """
        return self.receive_pipe.recv()


class DuplexCommunication(CommunicationInterface):
    def __init__(self, send_pipe, receive_pipe):
        """
        The Duplex communication object, use for inter-communication between
        the threads.

        Args:
            send_pipe (multiprocessing.Pipe): The pipe that will be used to
                send data.
            receive_pipe (multiprocessing.Pipe): The pipe that will be used to
                receive data from the adjacent process.
        """
        self.send_pipe = send_pipe
        self.receive_pipe = receive_pipe

    def send(self, data):
        """
        Call to send data.

        Args:
            data (object): Any data that can be pickled.
        """
        self.send_pipe.send(data)

    def receive(self):
        """
        Call to receive data

        Returns:
            object: Any data that can be pickled.
        """
        return self.receive_pipe.recv()


class SimplexError(Exception):
    """
    The SimplexError is a simple exception that is thrown when someone
    calls a simplex as a duplex object. Helps the interface determine whether
    the directions of the communication object. This may go away in the future.
    """
    pass
