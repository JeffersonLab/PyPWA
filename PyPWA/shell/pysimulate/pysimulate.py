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
This line is green in PyCharm, however in Github its blue.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import plugins
from shell.pysimulate import _libs

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Simulator(plugins.Main):

    __data_loader = None  # type: _libs.DataHandler
    __program_type = None  # type: str
    __intensity_processing = None  # type: _libs.Intensities
    __rejection_processing = None  # type: _libs.RejectionList

    def __init__(
            self, data_loader, the_type, kernel_processing=None,
            function_loader=None, parameters=None, max_intensity=None
    ):
        self.__data_loader = data_loader
        self.__program_type = the_type

        if the_type == "full" or the_type == "intensities":
            self.__setup_intensity_processing(
                function_loader, kernel_processing, parameters
            )
        elif the_type == "weighting":
            self.__setup_rejection_method(data_loader.data, max_intensity)

    def __setup_intensity_processing(self, functions, processing, parameters):
        self.__intensity_processing = _libs.Intensities(
            self.__data_loader, functions, processing, parameters
        )

    def __setup_rejection_method(self, intensities, max_intensity):
        self.__rejection_processing = _libs.RejectionList(
            intensities, max_intensity
        )

    def start(self):
        if self.__program_type == "full":
            self.__full_program_run()
        elif self.__program_type == "intensities":
            self.__intensity_program()
        elif self.__program_type == "weighting":
            self.__rejection_program()
        else:
            self.__raise_program_type_error()

    def __full_program_run(self):
        self.__intensity_processing.calc_intensities()
        self.__setup_rejection_method(
            self.__intensity_processing.processed_intensities,
            self.__intensity_processing.max_intensity
        )
        self.__rejection_program()

    def __intensity_program(self):
        self.__intensity_processing.calc_intensities()
        self.__data_loader.write_intensity_data(
            self.__intensity_processing.processed_intensities,
            self.__intensity_processing.max_intensity
        )

    def __rejection_program(self):
            self.__rejection_processing.rejection_method()
            self.__data_loader.write_rejection_list(
                self.__rejection_processing.rejection_list
            )

    def __raise_program_type_error(self):
        error = "The type is not set correctly! Found: %s but expected " \
                "either full, intensities, or weighting." % \
                repr(self.__program_type)

        raise ValueError(error)
