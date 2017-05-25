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
General Objects needed for PySimulate
-------------------------------------
A collection of objects are defined here that influence how the PySimulate 
works. All here is the true main logic of the program.

- DataHandler - takes the data objects, data location, and save location, 
  the providing access to whatever data it can load, and exposing  methods 
  that will handle to writing of all the different types of data the 
  simulation object would need written.

- Intensities - calculates the intensities using the provided processing 
  function and setup.

- RejectionList - takes an array of calculated intensities along with a max 
  intensity, normalizes the intensities, then using the Rejection Method, 
  randomly throws out events.
"""

import io
import random
import time
from typing import Dict

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import plugins
from PyPWA.shell import loaders
from PyPWA.shell.pysimulate import _processing

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class DataHandler(loaders.DataLoading):

    def __init__(self, data_parser, data_location, save_name):
        # type: (plugins.DataParser, str, str) -> None
        super(DataHandler, self).__init__(data_parser, data_location)
        self.__save_location = save_name

    def write_intensity_data(self, intensities, max_intensity):
        # type: (numpy.ndarray, float) -> None
        self.__write_intensity_array(intensities)
        self.__write_max_intensity(max_intensity)

    def __write_intensity_array(self, intensities):
        # type: (numpy.ndarray) -> None
        save_location = self.__save_location + "_intensities.txt"
        self.write(save_location, intensities)

    def __write_max_intensity(self, max_intensity):
        # type: (float) -> None
        save_location = self.__save_location + "_max.txt"
        with io.open(save_location, "w") as stream:
            stream.write(str(max_intensity))

    def write_rejection_list(self, rejection_list):
        # type: (numpy.ndarray) -> None
        rejection_list_name = self.__save_location + "_rejection.txt"
        self.write(rejection_list_name, rejection_list)


class Intensities(object):

    def __init__(
            self,
            data_loader,  # type: DataHandler
            function_loader,  # type: loaders.FunctionLoader
            processing,  # type: plugins.KernelProcessing
            parameters  # type: Dict[str, float]
    ):
        self.__data_loader = data_loader
        self.__function_loader = function_loader
        self.__processing = processing
        self.__parameters = parameters

        self.__found_intensities = None  # type: numpy.ndarray
        self.__max_intensity = None  # type: float

    def calc_intensities(self):
        self.__load_processing_module()
        self.__process_intensities()

    def __load_processing_module(self):
        the_kernel = _processing.IntensityKernel(
            self.__function_loader.setup, self.__function_loader.process,
            self.__parameters
        )
        the_interface = _processing.IntensityInterface()

        self.__processing.main_options(
            self.__get_kernel_data(), the_kernel, the_interface
        )

    def __get_kernel_data(self):
        # type: () -> Dict[str, numpy.ndarray]
        return {"data": self.__data_loader.data}

    def __process_intensities(self):
        operational_interface = self.__processing.fetch_interface()
        self.__found_intensities, self.__max_intensity = \
            operational_interface.run()

    @property
    def processed_intensities(self):
        # type: () -> numpy.ndarray
        return self.__found_intensities

    @property
    def max_intensity(self):
        # type: () -> float
        return self.__max_intensity


class RejectionList(object):

    __RANDOM = random.SystemRandom(time.gmtime())

    def __init__(self, intensities, max_intensity):
        # type: (numpy.ndarray, float) -> None
        self.__intensities = intensities
        self.__max_intensity = max_intensity

        self.__rejection_list = None  # type: numpy.ndarray
        self.__set_rejection_list()

    def __set_rejection_list(self):
        array_length = len(self.__intensities)
        self.__rejection_list = numpy.zeros(shape=array_length, dtype=bool)

    def rejection_method(self):
        self.__normalize_intensities()
        self.__loop_over_intensities()

    def __normalize_intensities(self):
        self.__intensities = self.__intensities / self.__max_intensity

    def __loop_over_intensities(self):
        for index, event in enumerate(self.__intensities):
            if event > self.__RANDOM.random():
                self.__rejection_list[index] = True

    @property
    def rejection_list(self):
        # type: () -> numpy.ndarray
        return self.__rejection_list
