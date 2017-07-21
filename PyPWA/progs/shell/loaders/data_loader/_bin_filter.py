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

"""

import warnings
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.progs.shell.loaders.data_loader import _dataset_storage

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _FilterDataset(object):

    __DATASET_FILTER_NAMES = [
        'data', 'binned', 'qfactor', 'expected values', 'event errors'
    ]

    def __init__(self):
        self.__initial_dataset = None  # type: _dataset_storage.DataStorage
        self.__zero_indexes = None  # type: numpy.ndarray
        self.__new_dataset = None  # type: _dataset_storage.DataStorage

    def filter(self, dataset):
        # type: (_dataset_storage.DataStorage) -> _dataset_storage.DataStorage
        self.__initial_dataset = dataset
        self.__get_zero_indexes()
        self.__create_new_dataset()
        return self.__new_dataset

    def __get_zero_indexes(self):
        locations = numpy.where(self.__initial_dataset.binned == 0.)
        self.__zero_indexes = numpy.ravel(locations)

    def __create_new_dataset(self):
        self.__new_dataset = _dataset_storage.DataStorage()
        self.__iterate_over_dataset_names()
        self.__pass_extra_values()

    def __iterate_over_dataset_names(self):
        for dataset_name in self.__DATASET_FILTER_NAMES:
            self.__filter_dataset_name(dataset_name)

    def __filter_dataset_name(self, dataset_name):
        # type: (str) -> None
        extracted_array = getattr(self.__initial_dataset, dataset_name)
        filtered_array = numpy.delete(extracted_array, self.__zero_indexes)
        setattr(self.__new_dataset, dataset_name, filtered_array)

    def __pass_extra_values(self):
        self.__new_dataset.single_array = self.__initial_dataset.single_array
        self.__new_dataset.monte_carlo = self.__initial_dataset.monte_carlo


class BinFilter(object):

    def __init__(self):
        self.__filter_utility = _FilterDataset()

    def __call__(self, dataset):
        # type: (_dataset_storage.DataStorage) -> _dataset_storage.DataStorage
        if self.__bins_have_zeros(dataset):
            self.__warn_user_about_dataset(dataset)
            return self.__filter_data_set(dataset)
        else:
            return dataset

    def __bins_have_zeros(self, dataset):
        # type: (_dataset_storage.DataStorage) -> bool
        return numpy.any(dataset.binned == 0.)

    @staticmethod
    def __warn_user_about_dataset(dataset):
        # type: (_dataset_storage.DataStorage) -> None
        number_of_zero_bins = len(dataset.binned[dataset.binned == 0.])
        warnings.warn(
            "Removing %f events from dataset where bin value is zero." %
            number_of_zero_bins
        )

    def __filter_data_set(self, dataset):
        # type: (_dataset_storage.DataStorage) -> _dataset_storage.DataStorage
        return self.__filter_utility.filter(dataset)
