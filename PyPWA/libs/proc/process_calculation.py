"""
Actual process objects are defined here
"""
import multiprocessing
from PyPWA.libs.proc import process_communication

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


class DuplexProcess(multiprocessing.Process):
    daemon = True

    def __init__(self, kernel, communication):
        super(DuplexProcess, self).__init__()
        self.kernel = kernel
        self.communication = communication

    def run(self):
        self.kernel.setup()
        while True:
            value = self.communication.recv()
            if value == "DIE":
                break
            elif value == "IGNORE":
                pass
            else:
                self.communication.send(self.kernel.process(value))
        return 0


class SimplexProcess(multiprocessing.Process):
    daemon = True

    def __init__(self, single_kernel, communication):
        super(SimplexProcess, self).__init__()
        self.kernel = single_kernel
        self.communication = communication

    def run(self):
        self.kernel.setup()
        self.communication.send(self.kernel.process())
        return 0


class SimplexCalculationFactory(object):
    def __init__(self, kernel, count):
        self._kernel = kernel
        self._count = count
        self._processes = []
        self._receives = []

    def build(self):
        sends, self._receives = process_communication.SimplexFactory(self._count)

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
        self._main_com, process_com = process_communication.DuplexFactory(self._count)

        for kernel, process_com in zip(self._kernel, process_com):
            self._processes.append(DuplexProcess(kernel, process_com))

        return self.processed

    @property
    def processed(self):
        return [self._processes, self._main_com]