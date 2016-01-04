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


class ProcessPipes(object):
    """Sets up pipes for Processes"""

    @staticmethod
    def return_pipes(num_pipes):
        """Returns pipes
        Args:
            num_pipes (int): Number of pipes to return
        Returns:
            list of lists: [[send pipes], [receive pipes] ]
        """
        send_to = []
        receive_from = []

        for x in range(num_pipes):
            receive, send = multiprocessing.Pipe(False)
            send_to.append(send)
            receive_from.append(receive)
        return [send_to, receive_from]
