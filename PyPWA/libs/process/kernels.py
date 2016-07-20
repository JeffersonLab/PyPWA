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
This file holds the kernels that need to be extended so that other plugins
and developers can use the process method.
"""

from PyPWA.libs.process import _communication
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

"""
Since the core requires a name, and we like to keep things as consistent
as possible, we define the core name here as a global definition that any
module inside the package can import. This means that if we decide to
change the name in the future our lives will be much easier.
"""

# The name for the module externally.
MODULE_NAME = "Builtin Multiprocessing"


class AbstractInterface(object):

    def __init__(self, is_duplex):
        """
        This is kernel that will run inside the Interface object, this
        object will be called every time the run method of the interface
        is called.

        Args:
            is_duplex (bool): Defines whether the object is duplex or not.
                Is needed so that the foreman knows to call for duplex or
                simplex processes. True if is duplex, False for simplex.
        """
        self.is_duplex = is_duplex

    def run(self, communicator, args):
        """
        Method that is called by the interface. This will be the method
        that you will use when you want to call something that

        Args:
            communicator (_communication._CommunicationInterface): This
                is how the interface will communicate to the threads. If
                duplex is set to true this will be able to send and
                receive data, if is false than will be able to receive
                data only.
            args: This will be whatever you sent to the run method,
                whatever you sent to the method will be packaged together
                here as a list.

        Returns:
            This can return whatever the developer needs it to return,
            there are no limitations.

        Raises:
            NotImplementedError: This is raised if this method isn't
            overwritten by the developer before the method is sent to the
            Interface Object.
        """
        raise NotImplementedError("The run method must be extended!")


class AbstractKernel(object):
    """
    This is the main kernel that is used inside the process. This kernel
    needs to be nested with all the information that it needs in order to
    run before it is sent to the foreman to be nested inside the
    processes.
    """

    def setup(self):
        """
        This method will be called once before any processing occurs, if
        there is any logic that needs to be executed once per thread to
        set up the process before any processing occurs that logic needs
        to be placed here.

        Note:
            This might have a return value of 1 for failure in the future
            and a value of 0 for success so that the process can crash
            silently and handle the error properly. This will be discussed
            further.

        Returns:
            Nothing. No return value will be handled here.

        Raises:
            NotImplementedError: This will be raised if the developer
                failed to extend the method.
        """
        raise NotImplementedError("The setup method must be extended!")

    def process(self, data=False):
        """
        This method will be called every single time the process receives
        data from the main process.

        Args:
            data (Optional): Anything that you send out to all threads
                through the interface object will be received here.

        Returns:
            Anything that is pickle-able that you want to send back to
            your main thread. This excludes things like functions and
            objects.

        Raises:
            NotImplementedError: This will be raised if the developer
                failed to extend the method.
        """
        raise NotImplementedError("The process method must be extended!")
