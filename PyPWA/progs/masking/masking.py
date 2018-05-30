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
Masking Utility
---------------
- _DataPackage - Loads the iterators and masks for the program.
- Masking - Masks and/or translates the data.
"""

import enum
import logging
import warnings
from typing import List
from typing import Optional as Opt

import numpy
import tqdm

from PyPWA.libs import configuration_db
from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.components.data_processor import file_processor
from PyPWA.libs.components.data_processor import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class MaskType(enum.Enum):
    AND = 1
    OR = 2
    XOR = 3


class _DataPackage(object):

    def __init__(self):
        # type: (...) -> None
        self.__reader = None  # type: data_templates.Reader
        self.__writer = None  # type: data_templates.Writer
        self.__data_processor = file_processor.DataProcessor()
        self.__db = configuration_db.Connector()
        self.__setup_data()

    def __setup_data(self):
        # type: () -> None
        input_file = Path(self.__db.read("masking", "input"))
        output_file = Path(self.__db.read("masking", "output"))
        masking_info = self.__db.read("masking", "mask")

        if isinstance(masking_info, type(None)):
           masking_file = masking_info
        else:
            masking_file = [Path(mask) for mask in masking_info]

        self.__load_reader(input_file)
        self.__load_writer(output_file)
        self.__setup_mask_array(masking_file)

    def __load_reader(self, input_file):
        # type: (Path) -> None
        self.__reader = self.__data_processor.get_reader(input_file)

    def __load_writer(self, output_file):
        # type: (Path) -> None
        self.__writer = self.__data_processor.get_writer(
            output_file, self.__reader.is_particle_pool
        )

    def __setup_mask_array(self, masking_file):
        # type: (Opt[List[Path]]) -> None

        if masking_file:
            self.__mask = self.__load_masking_files(masking_file)
        else:
            self.__mask = numpy.ones(len(self.__reader), dtype=bool)

    def __load_masking_files(self, masking_files):
        # type: (List[Path]) -> numpy.ndarray
        mask = None  # type: numpy.ndarray
        for file in masking_files:
            if isinstance(mask, type(None)):
                mask = self.__data_processor.parse(file)
            else:
                new_mask = self.__data_processor.parse(file)
                mask = self.__combine_mask_files(mask, new_mask)
        return mask

    def __combine_mask_files(self, current_mask, new_mask):
        # type: (numpy.ndarray, numpy.ndarray) -> numpy.ndarray
        mask_type = self.__db.read("masking", "mask type")
        if mask_type == MaskType.OR:
            return numpy.logical_or(current_mask, new_mask)
        elif mask_type == MaskType.XOR:
            return numpy.logical_xor(current_mask, new_mask)
        else:
            return numpy.logical_and(current_mask, new_mask)

    @property
    def reader(self):
        # type: () -> data_templates.Reader
        return self.__reader

    @property
    def mask(self):
        # type: () -> numpy.ndarray
        return self.__mask

    @property
    def writer(self):
        # type: () -> data_templates.Writer
        return self.__writer


class Masking(object):

    __LOGGER = logging.getLogger(__name__ + ".Masking")

    def __init__(self):
        # type: (...) -> None
        self.__data = _DataPackage()

    def start(self):
        self.__complain_to_user()
        self.__try_to_mask()

    def __complain_to_user(self):
        if len(self.__data.reader) < len(self.__data.mask):
            warnings.warn("Mask is larger than data events.")
        elif len(self.__data.reader) > len(self.__data.mask):
            self.__LOGGER.critical(
                "Mask is smaller than data events! Masker *will* crash!!"
            )

    def __try_to_mask(self):
        try:
            self.__mask()
        except Exception as error:
            raise error
        finally:
            self.__close_file_handles()

    def __mask(self):
        data_with_progress = tqdm.tqdm(self.__data.reader, unit="events")
        for index, value in enumerate(data_with_progress):
            print(index, len(data_with_progress), len(self.__data.mask))
            if self.__data.mask[index]:
                self.__data.writer.write(value)

    def __close_file_handles(self):
        self.__data.writer.close()
        self.__data.reader.close()
