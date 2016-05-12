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
This file holds the kernels that need to be extended so that other plugins and
developers can use the process method.
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


class AbstractInterface(object):

    def __init__(self, is_duplex):
        """
        This is kernel that will run inside the Interface object, this object
        will be called every time the run method of the interface is called.

        Note:
            This might be replaced through extension, we might require
            developers in the future to extend the Interface directly and define
            the run object.

        Args:
            is_duplex (bool): Defines whether the object is duplex or not.
                Is needed so that the foreman knows to call for duplex or
                simplex processes. True if is duplex, False for simplex.
        """
        self.is_duplex = is_duplex

    def run(self, communicator, args):
        """
        Method that is called by the interface. This will be the method that
        you will use when you want to call something that

        Args:
            communicator (_communication.CommunicationInterface): This is how the
                interface will communicate to the threads. If duplex is set to
                true this will be able to send and receive data, if is false
                than will be able to receive data only.
            args: This will be whatever you sent to the run method, whatever
                you sent to the method will be packaged together here as a list.

        Returns:
            This can return whatever the developer needs it to return, there
            are no limitations.

        Raises:
            NotImplementedError: This is raised if this method isn't overwritten
            by the developer before the method is sent to the Interface Object.
        """
        raise NotImplementedError("The run method must be extended!")


class AbstractKernel(object):
    """
    This is the main kernel that is used inside the process. This kernel needs
    to be nested with all the information that it needs in order to run before
    it is sent to the foreman to be nested inside the processes.
    """

    def setup(self):
        # function before the initial launch of PyPWA 2.
        """
        This method will be called once before any processing occurs, if there
        is any logic that needs to be executed once per thread to set up the
        process before any processing occurs that logic needs to be placed
        here.

        Note:
            This might have a return value of 1 for failure in the future and
            a value of 0 for success so that the process can crash silently and
            handle the error properly. This will be discussed further.

        Returns:
            Nothing. No return value will be handled here.

        Raises:
            NotImplementedError: This will be raised if the developer failed to
                extend the method.
        """
        raise NotImplementedError("The setup method must be extended!")

    def process(self, data):
        """
        This method will be called every single time the process receives data
        from the main process.

        Args:
            data: Anything that you sent out to all threads will come through
                here.

        Returns:
            Anything that is pickle-able that you want to send back to your
            main thread. This excludes things like functions and objects.

        Raises:
            NotImplementedError: This will be raised if the developer failed to
                extend the method.
        """
        raise NotImplementedError("The process method must be extended!")
