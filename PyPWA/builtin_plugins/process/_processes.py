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
The processes and their factories are defined here. The current supported
methods are Duplex for worker processes and Simplex for offload processes.
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


class DuplexProcess(multiprocessing.Process):

    daemon = True  # When true, processes will die with main
    _kernel = None
    _communicator = None

    def __init__(self, index, kernel, communicator):
        super(DuplexProcess, self).__init__()
        self._kernel = kernel
        self._kernel.processor_id = index
        self._communicator = communicator

    def run(self):
        self._kernel.setup()
        self._loop()
        return 0

    def _loop(self):
        while True:
            value = self._communicator.receive()
            if value == "DIE":
                break
            else:
                self._communicator.send(self._kernel.process(value))


class SimplexProcess(multiprocessing.Process):

    daemon = True  # When true, processes will die with main
    _kernel = None
    _communicator = None

    def __init__(self, index, single_kernel, communicator):
        super(SimplexProcess, self).__init__()
        self._kernel = single_kernel
        self._kernel.processor_id = index
        self._communicator = communicator

    def run(self):
        self._kernel.setup()
        self._communicator.send(self._kernel.process())
        return 0
