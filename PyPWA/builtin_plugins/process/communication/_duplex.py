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
Duplex object for the communication factory.
"""

import multiprocessing

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.process.communication import _interface

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _DuplexCommunication(_interface._CommunicationInterface):

    _send_pipe = None  # type: multiprocessing.Pipe
    _receive_pipe = None  # type: multiprocessing.Pipe

    def __init__(self, send_pipe, receive_pipe):
        self._send_pipe = send_pipe
        self._receive_pipe = receive_pipe

    def send(self, data):
        self._send_pipe.send(data)

    def receive(self):
        return self._receive_pipe.recv()
