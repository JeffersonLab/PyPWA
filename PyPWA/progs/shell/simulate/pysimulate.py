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
The Simulation program, this object simply routes the data around depending
on the type of program execution passed to it, the actual logic for the 
program exists in _libs.py
"""

import logging
from typing import Dict, Union
from typing import Optional as Opt

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import common
from PyPWA.libs.interfaces import kernel
from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.simulate import _libs

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Simulator(common.Main):

    __LOGGER = logging.getLogger(__name__ + ".Simulator")

    def __init__(
            self,
            data_loader,  # type: _libs.DataHandler
            the_type,   # type: Union["full", "intensities", "weighting"]
            kernel_processing=None,  # type: Opt[kernel.KernelProcessing]
            function_loader=None,  # type: Opt[loaders.FunctionLoader]
            parameters=None,  # type: Opt[Dict[str, numpy.float64]]
            max_intensity=None  # type: Opt[numpy.float64]
    ):
        # type: (...) -> None
        self.__data_loader = data_loader
        self.__program_type = the_type
        self.__kernel_processing = kernel_processing
        self.__function_loader = function_loader
        self.__parameters = parameters
        self.__max_intensity = max_intensity

        self.__intensity_calc = None  # type: _libs.Intensities
        self.__rejection_calc = None  # type: _libs.RejectionList
        self.__intensity_array = None  # type: numpy.ndarray

    def start(self):
        if self.__program_type == "full":
            self.__full_program_run()
        elif self.__program_type == "intensities":
            self.__intensity_program()
        elif self.__program_type == "weighting":
            self.__rejection_program()
        else:
            raise ValueError("Unknown type %s" % self.__program_type)

    def __full_program_run(self):
        self.__setup_intensity_calc()
        self.__intensity_calc.calc_intensities()
        self.__set_intensities_from_intensity_calc()
        self.__setup_rejection_calc()
        self.__rejection_calc.rejection_method()
        self.__write_rejection_data()

    def __setup_intensity_calc(self):
        self.__LOGGER.debug("Setting up Intensity Calculation.")
        self.__intensity_calc = _libs.Intensities(
            self.__data_loader, self.__function_loader,
            self.__kernel_processing, self.__parameters
        )

    def __set_intensities_from_intensity_calc(self):
        self.__max_intensity = self.__intensity_calc.max_intensity
        self.__intensity_array = self.__intensity_calc.processed_intensities

    def __setup_rejection_calc(self):
        self.__LOGGER.debug("Setting up Rejection Method.")
        self.__rejection_calc = _libs.RejectionList(
            self.__intensity_array, self.__max_intensity
        )

    def __write_rejection_data(self):
        self.__data_loader.write_rejection_list(
            self.__rejection_calc.rejection_list
        )

    def __intensity_program(self):
        self.__setup_intensity_calc()
        self.__intensity_calc.calc_intensities()
        self.__write_intensity_data()

    def __rejection_program(self):
        self.__intensity_array = self.__data_loader.data
        self.__setup_rejection_calc()
        self.__rejection_calc.rejection_method()
        self.__write_rejection_data()

    def __write_intensity_data(self):
        self.__data_loader.write_intensity_data(
            self.__intensity_calc.processed_intensities,
            self.__intensity_calc.max_intensity
        )

