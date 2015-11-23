"""
Handles comunication for processes
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

from abc import ABCMeta, abstractmethod
import multiprocessing

class ProcessPipes(object):
    """Sets up pipes for Processes"""

    def return_pipes(self, num_pipes):
        """Returns pipes
        Args:
            num_pipes (int): Number of pipes to return
        Returns:
            list of lists: [[send pipes], [recieve pipes] ]
        """
        send_to = []
        recieve_from = []

        for x in range(num_pipes):
            recieve, send = multiprocessing.Pipe(False)
            send_to.append(send)
            recieve_from.append(recieve)
        return [ send_to, recieve_from ]
