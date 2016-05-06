"""
Multiprocessing Calculation
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

from PyPWA.libs.proc import calculation_tools, process_calculation, process_communication


class SimplexCalculationFactory(object):
    def __init__(self, kernel, count):
        self._kernel = kernel
        self._count = count
        self._processes = []
        self._receives = []

    def build(self):
        sends, self._receives = process_communication.SingleFactory(self._count)

        for kernel, send in zip(self._kernel, sends):
            self._processes.append(process_calculation.SimplexProcess(kernel, send))

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
            self._processes.append(process_calculation.DuplexProcess(kernel, process_com))

        return self.processed

    @property
    def processed(self):
        return [self._processes, self._main_com]


class DuplexProcessInterface(object):
    def __init__(self, run_kernel, duplex_com):
        self._kernel = run_kernel
        self._com = duplex_com

    def run(self, *args):
        return self._kernel.run(self._com, args)

    def stop(self):
        """Shuts down processes"""
        for pipe in self._com:
            pipe.send("DIE")
