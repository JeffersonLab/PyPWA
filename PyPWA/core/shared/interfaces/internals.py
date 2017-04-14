#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Where the internal operation of the plugins are located.
--------------------------------------------------------
These interfaces reflect the internal design of the plugins, these should be 
used when you are defining a portion of a plugin that will interact with 
other plugins.

- Reader - The reader object that is expected to be returned by the 
  DataIterator.

- Writer - The writer object that is expected to be returned by the 
  DataIterator.
  
- ProcessInterface - This is the interface that is expected from 
  KernelProcessing's fetch_interface method. This is the main interface 
  between the kernels and the executing program.
  
- Kernel - The kernel of code that is expected to be sent to the 
  Kernel Processing plugins.

- KernelInterface - This defines how data returned by each of the kernels 
  should be processed.
  
- OptimizerOptionParser - This is to process the parameters by the 
  optimizer to be sent to the user's kernel or code. This is to either 
  package values in a easy to use dictionary and/or to remove extra 
  trailing information.
  
- LikelihoodTypes - An enumeration of the various likelihoods that are used 
  internally. OTHER, LOG_LIKELIHOOD, and CHI_SQUARED.
"""

import enum
import numpy

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Reader(object):

    def next(self):
        """
        Called to get the next event from the reader.
        
        :return: A single event.
        :rtype: numpy.ndarray
        """
        raise NotImplementedError()

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """
        Should close any open objects or streams.
        """
        raise NotImplementedError()


class Writer(object):

    def write(self, data):
        """
        Should write the received event to the stream.
        
        :param numpy.ndarray data: The event data stored in a numpy array. 
        """
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """
        Should close the stream and any open streams or objects.
        """
        raise NotImplementedError()


class ProcessInterface(object):

    def run(self, *args):
        """
        This function will start the processing of the processes, whatever was
        passed through the kernel will be started with this method.
        
        :param args: Anything that you want to pass to your kernel.
        :return: The value kernel interface.
        """
        raise NotImplementedError

    @property
    def previous_value(self):
        """
        The previous value received from the kernel interface.
        
        :return: Previous calculated value.
        """
        raise NotImplementedError

    def stop(self, force=False):
        """
        Should stop all process, threads, etc, that are being used to 
        calculate.
        
        :param bool force: whether children should be stopped gently or 
        violently murdered.
        """
        raise NotImplementedError

    @property
    def is_alive(self):
        """
        Should return whether the children are still alive or have been 
        shutdown.
        
        :return: The state of the processes.
        :rtype: bool
        """
        raise NotImplementedError


class Kernel(object):

    # process_id should be set by the Kernel Processing plugin.
    processor_id = None  # type: int

    def setup(self):
        """
        Anything that should be setup in the thread or process should be 
        put here, this will be called only once before any calculation begins.
        """
        raise NotImplementedError()

    def process(self, data=False):
        """
        The actual calculation or function of the program, can optionally 
        support values from the main thread / process.
        
        :param data: Any data that you want to pass to the kernel.
        :return: The final value or object that should be sent back to the 
        main thread.
        """
        raise NotImplementedError()


class KernelInterface(object):

    # is_duplex controls whether the kernel will shutdown after its first
    # run or if the kernel will wait for more information. If this is true
    # the kernel will only be able to receive data and will shutdown after
    # its first run; however, if this is true then the kernel will stay
    # running and waiting for a value from the interface indefinitely until
    # they are shutdown manually.
    is_duplex = False

    def run(self, communicator, args):
        """
        The method that will be called to begin the calculation. This is 
        the interface between the kernels and the calling object.
        
        :param communicator: A list of objects that will be used to 
        communicate with the kernels.
        :param args: Any values that are sent to the main interface.
        :return: Whatever value that is calculated locally from the kernels.
        """
        raise NotImplementedError("The run method must be extended!")


class OptimizerOptionParser(object):

    # A simple multiplier that will be multiplied to the final result of
    # every run call.
    multiplier = 1

    def convert(self, passed_value):
        """
        This should take any value sent by optimizer and clean up the value 
        to something easier for the user to interact with if possible.
        
        :param passed_value: The object sent by the optimizer.
        :return: The cleaned up value.
        """
        raise NotImplementedError


class LikelihoodTypes(enum.Enum):
    OTHER = 1
    CHI_SQUARED = 2
    LOG_LIKELIHOOD = 3
