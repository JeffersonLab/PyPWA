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
The core definition of plugins and how they work.
-------------------------------------------------
All the different plugin types are defined here, these interfaces should be
extended when writing your own plugins so that your own plugin can replace
the internal plugins without any issues.

.. note::
   Some of these interfaces have a main method called "main_options",
   this method exists so that options not passed via the __init__ can be
   loaded into the object still before running. Typically this is for
   runtime variables and not for user variables.

- Optimizer - This is the interface for minimizer and maximizer alike.

- KernelProcessing - This defines how kernel processing works, simply,
  the kernel processing works by taking a kernel of code, a package of
  data, then using those to calculate more data. The interface to interact
  with the resulting processes, threads, etc, and the core kernel that you
  should expect to return are all in internals.py

- DataParser - This is a parser that will return a numpy array,
  or something that operates a lot like a numpy array. It is expected that
  all events will be returned at once, or a reference to all events. Should
  also be able to write data as well.

- DataIterator - This is more complex parser, this parser should be able to
  read and write a single event at a time, as such should be able to be used
  in iteration, or as a file handle.

- Main - This is a simple interface for the main objects.
"""

import enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional as Opt

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class BasePlugin(object):
    # Simply here for inheritance.
    pass


class Optimizer(BasePlugin):

    def main_options(self, calc_function, fitting_type=None):
        # type: (Callable[[Any], Any], Opt[internals.LikelihoodTypes]) -> None
        """
        The main options for the Optimizer, these are options that are
        typically needed for optimization, but due to the design of the
        program, these options can't be passed directly to the optimizer
        via its __init__ method.

        :param calc_function: The main runtime function for the program.
        This is often the likelihood, or amplitude, that needs to be
        optimized.
        :param internals.LikelihoodTypes fitting_type: One of the
        enumerations from likelihood types.
        """
        raise NotImplementedError

    def start(self):
        # type: () -> None
        """
        This should start all the actual processing and logic inside the
        optimizer, anything being started before this is called could cause
        an internal error.
        """
        raise NotImplementedError

    def return_parser(self):
        # type: () -> internals.OptimizerOptionParser
        """
        Since each optimizer is different, and as such sends and receives
        its arguments in a different way, this provides the object that
        will attempt to 'normalize' these arguments to make interact with
        them more transparent.

        :rtype: internals.OptimizerOptionParser
        :return: An object that extended the option parsing interface that
        will convert the received parameters.
        """
        raise NotImplementedError

    def save_extra(self, save_name):
        # type: (str) -> None
        """
        Takes whatever information the optimizer found and saves it using
        the supplied save_name.

        :param str save_name: The name of the file to save to, or the
        template of the name depending on the optimizer. The optimizer
        doesn't have to save all information to the file name provided
        explicitly, and can instead do save along the lines of
        "save_name_covariance" for example.
        """
        raise NotImplementedError


class KernelProcessing(BasePlugin):

    def main_options(
            self,
            data,  # type: Dict[str, numpy.ndarray]
            process_template,  # type: internals.Kernel
            interface_template  # type: internals.KernelInterface
    ):
        # type: (...) -> None
        """
        The main options for the KernelProcessor, these are options that are
        typically needed for processing, but due to the design of the
        program, these options can't be passed directly to the processor
        via its __init__ method.

        :param dict data: A dictionary with values being numpy arrays, each
        key should be loaded into the processing template as a public
        variable.
        :param internals.Kernel process_template: A predefined kernel that
        holds all the logic and static data needed to calculate the
        provided function. This static data does not include events,
        but instead data that should be needed no matter the event being
        calculated. Ex. the value of π.
        :param internals.KernelInterface interface_template: The definition
        of how the return values should be calculated from the kernels.
        This could be a simple as a Sum, or as complicated as you could want.
        """
        raise NotImplementedError

    def fetch_interface(self):
        # type: () -> internals.ProcessInterface
        """
        Returns the finished interface for the processing.

        :rtype: internals.ProcessInterface
        :return: Returns a finalized implementation to the processing
        kernel for the receiving object to use.
        """
        raise NotImplementedError


class DataParser(BasePlugin):

    def parse(self, text_file):
        # type: (str) -> numpy.ndarray
        """
        Called to read in the data from a file.

        :param str text_file: The path to the file to read.
        :return: All the data from the file.
        :rtype: numpy.ndarray
        """
        raise NotImplementedError

    def write(self, text_file, data):
        # type: (str, numpy.ndarray) -> None
        """
        Called to write a numpy array out to file.

        :param str text_file: The file to write the data out to.
        :param numpy.ndarray data: The array data to write.
        """
        raise NotImplementedError


class DataIterator(BasePlugin):

    def return_reader(self, text_file):
        # type: (str) -> internals.Reader
        """
        Returns an initialized reader for that text file.

        :param str text_file: The file to be read over.
        :return: An initialized reader.
        :rtype: internals.Reader
        """
        raise NotImplementedError

    def return_writer(self, text_file, data):
        # type: (str, numpy.ndarray) -> internals.Writer
        """
        Returns an initialized writer that will work with the data type.

        :param str text_file: Where to write the data.
        :param numpy.ndarray data: The array or event you want to write.
        :return: An initialized writer.
        :rtype: internals.Writer
        """
        raise NotImplementedError


class Main(BasePlugin):

    def start(self):
        # type: () -> None
        """
        This is the method that should start the execution on the main object.
        It is assumed that basic setup of the program has been done by this
        point, and this should simply start the function of the program.
        """
        raise NotImplementedError


class Types(enum.Enum):

    KERNEL_PROCESSING = 1
    OPTIMIZER = 2
    DATA_READER = 3
    DATA_PARSER = 4
    SKIP = 5
