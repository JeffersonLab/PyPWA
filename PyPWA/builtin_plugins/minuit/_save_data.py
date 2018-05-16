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
Saves Data for iMinuit in a way the User can interact with it
-------------------------------------------------------------

- _MakeTable - Makes the covariance table for the minimizer, also optionally
  prints out the table.

- _WriteData - takes all the essential data from the minimizer and saves to
  the disk.

- SaveData - the main object for saving data from iMinuit.
"""

import logging

import numpy
import tabulate

from PyPWA import Path


class _MakeTable(object):

    __logger = logging.getLogger(__name__ + "._MakeTable")

    __x = set()
    __y = set()
    __covariance = []

    __fancy_table = None
    __regular_table = None

    def make_tables(self, covariance_data):
        self.__clear_variables()
        self.__set_x_y_data(covariance_data)
        self.__set_covariance_with_data(covariance_data)
        self.__set_tables()

    def __clear_variables(self):
        self.__x.clear()
        self.__y.clear()
        self.__covariance[:] = []

    def __set_x_y_data(self, covariance_data):
        for field in covariance_data:
            self.__x.add(field[0])
            self.__y.add(field[1])

    def __set_covariance_with_data(self, covariance_data):
        for x in self.__x:
            row = [x]
            for y in self.__y:
                row.append(covariance_data[(x, y)])
            self.__covariance.append(row)

    def __set_tables(self):
        self.__fancy_table = tabulate.tabulate(
                self.__covariance, self.__y, "fancy_grid", numalign="center"
        )

        self.__regular_table = tabulate.tabulate(
                self.__covariance, self.__y, "grid", numalign="center"
        )

    def print_table(self):
        print("Covariance: \n")
        try:
            print(self.__fancy_table)
        except UnicodeEncodeError as system_error:
            print(self.__regular_table)
            self.__logger.info(
                "Unicode tables are not supported, falling back to regular"
            )
            self.__logger.debug(system_error, exc_info=True)

    @property
    def table(self):
        return self.__regular_table


class _WriteData(object):

    __save_location = None
    __covariance_data = None
    __final_value = None
    __values = None
    __table_data = None

    def __init__(
            self, save_location, covariance_data, final_value, values,
            table_data
    ):
        self.__save_location = save_location
        self.__covariance_data = covariance_data
        self.__final_value = final_value
        self.__values = values
        self.__table_data = table_data

    def write_data(self):
        self.__save_text_data()
        self.__save_numpy_data()

    def __save_text_data(self):
        new_path = Path(str(self.__save_location.stem + ".txt"))
        with open(str(new_path), "w") as stream:
            stream.write("Covariance.\n")
            stream.write(self.__table_data.table)
            stream.write("\n")
            stream.write("final value: " + str(self.__final_value))

    def __save_numpy_data(self):
        numpy.save(
            str(self.__save_location) + ".npy", {
                "covariance": self.__covariance_data,
                "fval": self.__final_value,
                "values": self.__values
            }
        )


class SaveData(object):
    __logger = logging.getLogger(__name__ + "._SaveData")
    __table = _MakeTable()
    __write_data = None  # type: _WriteData

    def save_data(self, save_location, covariance_data, final_value, values):
        self.__load_table(covariance_data)
        self.__print_table()
        self.__set_write_data(
            save_location, covariance_data, final_value, values
        )
        self.__save_data_to_file()

    def __load_table(self, covariance_data):
        self.__table.make_tables(covariance_data)

    def __print_table(self):
        self.__table.print_table()

    def __set_write_data(
            self, save_location, covariance_data, final_value, values
    ):
        self.__write_data = _WriteData(
            save_location, covariance_data, final_value, values, self.__table
        )

    def __save_data_to_file(self):
        self.__write_data.write_data()
