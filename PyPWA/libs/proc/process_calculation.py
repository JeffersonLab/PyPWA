"""
Actual process objects are defined here
"""
import multiprocessing

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
