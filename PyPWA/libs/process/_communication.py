#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This is an internal file that handles the communication between the main
process and the children processes. This file contains the factory that is
needed to build the needed number of pipes, and Duplex and Simplex Objects
so that offload process and worker processes can be generated.
"""

import multiprocessing

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class CommunicationFactory(object):
    """

    """

    @staticmethod
    def simplex_build(count):
        """
        When called this method will build the pipes and nest the into the
        SingleSend and SingleReceive objects to be sent to the main
        process and sub processes alike.

        Returns:
            list[list[SingleSend],list[SingleReceive]]
        """

        sends = [0] * count
        receives = [0] * count

        for pipe in range(count):
            receive, send = multiprocessing.Pipe(False)
            sends[pipe] = _SimplexSend(send)
            receives[pipe] = _SimplexReceive(receive)

        return [sends, receives]

    @staticmethod
    def duplex_build(count):
        """
        When called this method will build the pipes and nest them into
        the DuplexCommunication object to be sent to the main process and
        sub processes.

        Returns:
            list [list[_DuplexCommunication],list[_DuplexCommunication]]
        """
        main = [0] * count
        process = [0] * count

        for pipe in range(count):
            receive_one, send_one = multiprocessing.Pipe(False)
            receive_two, send_two = multiprocessing.Pipe(False)

            main[pipe] = _DuplexCommunication(send_one, receive_two)
            process[pipe] = _DuplexCommunication(send_two, receive_one)

        return [main, process]


class _CommunicationInterface(object):
    """
    This is a simple interface object for the communication objects to
    ensure that they are functioning in a predictable way. All
    communication objects extend this object.
    """

    def send(self, data):
        """
        Sends data to the opposite process, whether that is the children
        process or the parent process.

        Args:
            data: The data pickle-able the needs to be sent.

        Raises:
            NotImplementedError: If the objects are not replaced before
                being executed.
        """

        raise NotImplementedError(
            "Object fails to override the send method."
        )

    def receive(self):
        raise NotImplementedError(
            "Object fails to override the receive method"
        )


class _SimplexSend(_CommunicationInterface):

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

        raise SimplexError(
            "Communication Object is Simplex and doesn't support the "
            "receive method."
        )


class _SimplexReceive(_CommunicationInterface):

    def __init__(self, receive_pipe):
        """
        Simple Receive object

        Args:
            receive_pipe (multiprocessing.Pipe): The pipe that can be
                used to receive data
        """
        self.receive_pipe = receive_pipe

    def send(self, data):
        """
        Null call to send method.

        Raises:
            SimplexError: Simplex object can only receive.
        """
        raise SimplexError(
            "Communication Object is Simplex and doesn't support the send"
            " method."
        )

    def receive(self):
        """
        Call to fetch data from the pipe.

        Returns:
            object: Anything that can be pickled
        """
        return self.receive_pipe.recv()


class _DuplexCommunication(_CommunicationInterface):

    def __init__(self, send_pipe, receive_pipe):
        """
        The Duplex communication object, use for inter-communication
        between the threads.

        Args:
            send_pipe (multiprocessing.Pipe): The pipe that will be used
                to send data.
            receive_pipe (multiprocessing.Pipe): The pipe that will be
                used to receive data from the adjacent process.
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
    calls a simplex as a duplex object. Helps the interface determine
    whether the directions of the communication object. This may go away
    in the future.
    """
    pass
