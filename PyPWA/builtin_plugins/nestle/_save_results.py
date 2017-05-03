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
Saves Data for Nestle in a way the User can interact with it
------------------------------------------------------------

- _MakeTable - Makes the covariance table for the minimizer, also optionally   
  prints out the tables.
  
- _SaveData - takes all the essential data from the minimizer and saves to
  the disk. 

- SaveData - the main object for saving data from iMinuit.
"""

import numpy
import nestle
import tabulate


class _MakeTable(object):

    __fancy_mean_table = None
    __fancy_cov_table = None
    __regular_mean_table = None
    __regular_cov_table = None

    __covariance = None
    __means = None
    __index_list = list()
    __mean_list = list()
    __covariance_list = list()

    def make_tables(self, results):
        self.__clear_variables()
        self.__load_mean_and_covariance(results)
        self.__set_index_list()
        self.__create_mean_list()
        self.__create_covariance_list()
        self.__create_mean_tables()
        self.__create_covariance_tables()

    def __clear_variables(self):
        self.__covariance_list[:] = []
        self.__mean_list.clear[:] = []
        self.__index_list.clear[:] = []

    def __load_mean_and_covariance(self, results):
        self.__means, self.__covariance = nestle.mean_and_cov(
            results.samples, results.weights
        )

    def __set_index_list(self):
        self.__index_list = list(range(len(self.__covariance)))

    def __create_mean_list(self):
        for index, mean in enumerate(self.__means):
            row = [index, mean]
            self.__mean_list.append(row)

    def __create_covariance_list(self):
        for x in self.__index_list:
            row = [x]
            for y in self.__index_list:
                row.append(self.__covariance[x, y])
            self.__covariance_list.append(row)

    def __create_mean_tables(self):
        self.__fancy_mean_table = tabulate.tabulate(
            self.__mean_list, ["Mean"], "fancy_grid", numalign="center"
        )

        self.__regular_mean_table = tabulate.tabulate(
            self.__mean_list, ["Mean"], "grid", numalign="center"
        )

    def __create_covariance_tables(self):
        self.__fancy_cov_table = tabulate.tabulate(
            self.__covariance_list, self.__index_list, "fancy_grid",
            numalign="center"
        )

        self.__regular_cov_table = tabulate.tabulate(
            self.__covariance_list, self.__index_list, "grid",
            numalign="center"
        )

    def print_tables(self):
        try:
            print(self.__fancy_mean_table)
            print("Covariance: ")
            print(self.__fancy_cov_table)
        except UnicodeDecodeError:
            print(self.__regular_mean_table)
            print("Covariance: ")
            print(self.__regular_cov_table)

    @property
    def cov_table(self):
        return self.__regular_cov_table

    @property
    def mean_table(self):
        return self.__regular_mean_table


class _SaveData(object):

    @classmethod
    def save_data(cls, save_name, results, table):
        cls.__save_text_data(save_name, results, table)
        cls.__save_cov_data(save_name, results)

    @staticmethod
    def __save_text_data(save_name, results, table):
        with open(save_name + ".txt", "w") as stream:
            stream.write(results.summary())
            stream.write("\n\n")
            stream.write(table.mean_table)
            stream.write("\n\n")
            stream.write(table.cov_table)

    @staticmethod
    def __save_cov_data(save_name, results):
        mean, cov = nestle.mean_and_cov(results.samples, results.weights)
        numpy.save(save_name + ".npy", {"mean": mean, "cov": cov})


class SaveData(object):

    __tables = _MakeTable()

    def save_data(self, save_location, results):
        self.__print_summery(results)
        self.__make_tables(results)
        self.__print_tables()
        self.__save_data(save_location, results)

    @staticmethod
    def __print_summery(results):
        print(results.summary(), end="\n\n")

    def __make_tables(self, results):
        self.__tables.make_tables(results)

    def __print_tables(self):
        self.__tables.print_tables()

    def __save_data(self, save_location, results):
        _SaveData.save_data(save_location, results, self.__tables)
