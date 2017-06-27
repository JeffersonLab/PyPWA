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

import logging
import warnings
from typing import Optional as Opt

import numpy
import tqdm

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _DataPackage(object):

    def __init__(
            self,
            input_file,  # type: str
            masking_file,   # type: Opt[str]
            output_file,  # type: str
            parser,  # type: plugins.DataParser
            iterator  # type: plugins.DataIterator
    ):
        # type: (...) -> None
        self.__mask = None
        self.__writer = None
        self.__reader = None
        self.__iterator = iterator
        self.__setup_data(input_file, output_file, masking_file, parser)

    def __setup_data(self, input_file, output_file, masking_file, parser):
        # type: (str, str, Opt[str], plugins.DataParser) -> None
        self.__load_writer(input_file, output_file)
        self.__load_reader(input_file)
        self.__setup_masking_file(masking_file, parser)

    def __load_writer(self, input_file, output_file):
        # type: (str, str) -> None
        with self.__iterator.return_reader(input_file) as reader:
            self.__writer = self.__iterator.return_writer(
                output_file, reader.next()
            )

    def __load_reader(self, input_file):
        # type: (str) -> None
        self.__reader = self.__iterator.return_reader(input_file)

    def __setup_masking_file(self, masking_file, parser):
        # type: (Opt[str],  plugins.DataParser) -> None
        if masking_file:
            self.__mask = parser.parse(masking_file)
        else:
            self.__mask = numpy.ones(len(self.__reader), dtype=bool)

    @property
    def reader(self):
        # type: () -> internals.Reader
        return self.__reader

    @property
    def mask(self):
        # type: () -> numpy.ndarray
        return self.__mask

    @property
    def writer(self):
        # type: () -> internals.Writer
        return self.__writer


class Masking(plugins.Main):

    __LOGGER = logging.getLogger(__name__ + ".Masking")

    def __init__(
            self,
            input_file,  # type: str
            output_file,  # type: str
            parser,  # type: plugins.DataParser
            iterator,  # type: plugins.DataIterator
            masking_file=None  # type: Opt[str]
    ):
        # type: (...) -> None
        self.__data = _DataPackage(
            input_file, masking_file, output_file, parser, iterator
        )
        self.__output_file = output_file

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
            if self.__data.mask[index]:
                self.__data.writer.write(value)
