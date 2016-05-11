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
Actual process objects are defined here
"""
import multiprocessing
from PyPWA.libs.process import communication
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DuplexProcess(multiprocessing.Process):
    daemon = True

    def __init__(self, kernel, communicator):
        super(DuplexProcess, self).__init__()
        self._kernel = kernel
        self._communicator = communicator

    def run(self):
        self._kernel.setup()
        while True:
            value = self._communicator.recv()
            if value == "DIE":
                break
            elif value == "IGNORE":
                pass
            else:
                self._communicator.send(self._kernel.process(value))
        return 0


class SimplexProcess(multiprocessing.Process):
    daemon = True

    def __init__(self, single_kernel, communicator):
        super(SimplexProcess, self).__init__()
        self._kernel = single_kernel
        self._communicator = communicator

    def run(self):
        self._kernel.setup()
        self._communicator.send(self._kernel.process())
        return 0


class SimplexCalculationFactory(object):
    def __init__(self, kernel, count):
        self._kernel = kernel
        self._count = count
        self._processes = []
        self._receives = []

    def build(self):
        sends, self._receives = communication.SimplexFactory(self._count)

        for kernel, send in zip(self._kernel, sends):
            self._processes.append(SimplexProcess(kernel, send))

        return self.processed

    @property
    def processed(self):
        return [self._processes, self._receives]


class DuplexCalculationFactory(object):
    def __init__(self, kernel, count):
        self._kernel = kernel
        self._count = count
        self._processes = []
        self._main_com = []

    def build(self):
        self._main_com, process_com = communication.DuplexFactory(self._count)

        for kernel, process_com in zip(self._kernel, process_com):
            self._processes.append(DuplexProcess(kernel, process_com))

        return self.processed

    @property
    def processed(self):
        return [self._processes, self._main_com]