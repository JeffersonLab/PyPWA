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

"""

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ReaderInterfaceTemplate(object):

    def __init__(self, file_location):
        """

        Args:
            file_location:
        """
        self._the_file = file_location

    def reset(self):
        """

        Returns:

        """
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object reset properly when "
            "this method is called." % self.__class__.__name__
        )

    @property
    def next_event(self):
        """

        Returns:

        """
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object read in the next "
            "event properly when its called." % self.__class__.__name__
        )

    def next(self):
        return self.next_event

    def __next__(self):
        return self.next_event

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def previous_event(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object return the last "
            "value that was parsed." % self.__class__.__name__
        )

    def close(self):
        """

        Returns:

        """
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object return the last "
            "value that was parsed." % self.__class__.__name__
        )


class WriterInterfaceTemplate(object):

    def __init__(self, file_location):
        """

        Args:
            file_location:
        """
        self._the_file = file_location

    def write(self, data):
        """

        Args:
            data:

        Returns:

        """
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object write the data out "
            "to the disk correctly." % self.__class__.__name__
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """

        Returns:

        """
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object properly operated "
            "properly when its called" % self.__class__.__name__
        )


class InterfaceTemplate(object):
    """
    Template for interface objects to be handed off by the KernelProcessor
    """

    def run(self, *args):
        """

        Args:
            *args:

        Returns:

        """
        raise NotImplementedError

    @property
    def previous_value(self):
        raise NotImplementedError

    def stop(self, force=False):
        """

        Args:
            force:

        Returns:

        """
        raise NotImplementedError

    @property
    def is_alive(self):
        """

        Returns:

        """
        raise NotImplementedError


class AbstractKernel(object):
    """
    This is the main kernel that is used inside the process. This kernel
    needs to be nested with all the information that it needs in order to
    run before it is sent to the foreman to be nested inside the
    processes.
    """

    # The ID of the process to aid in ordering.
    processor_id = None

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
            data (Optional[tuple]): Anything that you send out to all
                threads through the interface object will be received
                here.

        Returns:
            Anything that is pickle-able that you want to send back to
            your main thread. This excludes things like functions and
            objects.

        Raises:
            NotImplementedError: This will be raised if the developer
                failed to extend the method.
        """
        raise NotImplementedError("The process method must be extended!")


class AbstractInterface(object):
    """
    This is kernel that will run inside the Interface object, this
    object will be called every time the run method of the interface
    is called.

    Args:
        is_duplex (bool): Defines whether the object is duplex or not.
            Is needed so that the foreman knows to call for duplex or
            simplex processes. True if is duplex, False for simplex.
    """

    is_duplex = False

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
            args (tuple): This will be whatever you sent to the run method
                packaged together as a list with its index matching the
                order of your arguments.

        Returns:
            This can return whatever the developer needs it to return,
            there are no limitations.

        Raises:
            NotImplementedError: This is raised if this method isn't
            overwritten by the developer before the method is sent to the
            Interface Object.
        """
        raise NotImplementedError("The run method must be extended!")


class MinimizerParserTemplate(object):
    """

    """

    def convert(self, passed_value):
        """

        Args:
            passed_value:

        Returns:

        """
        raise NotImplementedError
