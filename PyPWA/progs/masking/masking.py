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

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import common
from PyPWA.libs.interfaces import data_loaders

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class MaskType(enum.Enum):
    AND = 1
    OR = 2
    XOR = 3


class _DataPackage(object):

    def __init__(
            self,
            input_file,  # type: str
            masking_file,   # type: Opt[str]
            output_file,  # type: str
            parser,  # type: data_loaders.ParserPlugin
            iterator,  # type: data_loaders.IteratorPlugin
            mask_type=MaskType.AND  # type: MaskType
    ):
        # type: (...) -> None
        self.__mask = None
        self.__writer = None
        self.__reader = None
        self.__operation_type = mask_type
        self.__iterator = iterator
        self.__setup_data(input_file, output_file, masking_file, parser)

    def __setup_data(self, input_file, output_file, masking_file, parser):
        # type: (str, str, Opt[str], data_loaders.ParserPlugin) -> None
        self.__load_writer(input_file, output_file)
        self.__load_reader(input_file)
        self.__setup_mask_array(masking_file, parser)

    def __load_writer(self, input_file, output_file):
        # type: (str, str) -> None
        with self.__iterator.return_reader(input_file) as reader:
            self.__writer = self.__iterator.return_writer(
                output_file, reader.next()
            )

    def __load_reader(self, input_file):
        # type: (str) -> None
        self.__reader = self.__iterator.return_reader(input_file)

    def __setup_mask_array(self, masking_file, parser):
        # type: (Opt[List[str]],  data_loaders.ParserPlugin) -> None
        if masking_file:
            self.__mask = self.__load_masking_files(masking_file, parser)
        else:
            self.__mask = numpy.ones(len(self.__reader), dtype=bool)

    def __load_masking_files(self, masking_files, parser):
        # type: (List[str],  data_loaders.ParserPlugin) -> numpy.ndarray
        mask = None  # type: numpy.ndarray
        for file in masking_files:
            if isinstance(mask, type(None)):
                mask = parser.parse(file)
            else:
                new_mask = parser.parse(file)
                mask = self.__combine_mask_files(mask, new_mask)
        return mask

    def __combine_mask_files(self, current_mask, new_mask):
        # type: (numpy.ndarray, numpy.ndarray) -> numpy.ndarray
        if self.__operation_type == MaskType.OR:
            return numpy.logical_or(current_mask, new_mask)
        elif self.__operation_type == MaskType.XOR:
            return numpy.logical_xor(current_mask, new_mask)
        else:
            return numpy.logical_and(current_mask, new_mask)

    @property
    def reader(self):
        # type: () -> data_loaders.Reader
        return self.__reader

    @property
    def mask(self):
        # type: () -> numpy.ndarray
        return self.__mask

    @property
    def writer(self):
        # type: () -> data_loaders.Writer
        return self.__writer


class Masking(common.Main):

    __LOGGER = logging.getLogger(__name__ + ".Masking")

    def __init__(
            self,
            input_file,  # type: str
            output_file,  # type: str
            parser,  # type: data_loaders.ParserPlugin
            iterator,  # type: data_loaders.IteratorPlugin
            masking_file=None,  # type: Opt[str]
            mask_type=MaskType.AND  # type: MaskType
    ):
        # type: (...) -> None
        self.__data = _DataPackage(
            input_file, masking_file, output_file, parser, iterator, mask_type
        )

    def start(self):
        self.__complain_to_user()
        self.__mask()

    def __complain_to_user(self):
        if len(self.__data.reader) < len(self.__data.mask):
            warnings.warn("Mask is larger than data events.")
        elif len(self.__data.reader) > len(self.__data.mask):
            self.__LOGGER.critical(
                "Mask is smaller than data events! Masker *will* crash!!"
            )

    def __mask(self):
        data_with_progress = tqdm.tqdm(self.__data.reader, unit="events")
        for index, value in enumerate(data_with_progress):
            if not self.__data.mask[index]:
                self.__data.writer.write(value)
        self.__data.writer.close()
