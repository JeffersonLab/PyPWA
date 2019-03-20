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
Holds the different implementation interfaces that are needed to interface
data module.
"""

import enum
import numpy as npy
from typing import List

from PyPWA import Path, AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class DataType(enum.Enum):
    BASIC = 0
    STRUCTURED = 1
    TREE_VECTOR = 2


class Memory:

    def parse(self, filename: Path, precision: npy.dtype) -> npy.ndarray:
        raise NotImplementedError

    def write(self, filename: Path, data: npy.ndarray):
        raise NotImplementedError


class ReadPackage:

    def get_reader(self):
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError

    def get_bytes(self):
        raise NotImplementedError

    def get_event_count(self):
        raise NotImplementedError


class Reader(object):

    def next(self) -> npy.ndarray:
        """
        Called to get the next event from the reader.

        :return: A single event.
        :rtype: numpy.ndarray
        """
        raise NotImplementedError

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __len__(self):
        return self.get_event_count()

    def __exit__(self, *args):
        self.close()

    def get_event_count(self) -> int:
        """
        Called to get the total number of events in the file.

        :return: Count of the events
        :rtype: int
        """
        raise NotImplementedError

    def reset(self):
        """
        Resets the reader back to the first event
        """
        raise NotImplementedError

    def close(self):
        """
        Should close any open objects or streams.
        """
        raise NotImplementedError

    @property
    def is_particle_pool(self) -> bool:
        return False

    @property
    def fields(self) -> List[str]:
        raise NotImplementedError


class Writer(object):

    def write(self, data: npy.ndarray):
        """
        Should write the received event to the stream.

        :param numpy.ndarray data: The event data stored in a numpy array.
        """
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """
        Should close the stream and any open streams or objects.
        """
        raise NotImplementedError


class ReadTest(object):

    def can_read(self, filename: Path) -> bool:
        raise NotImplementedError


class DataPlugin:

    @property
    def plugin_name(self) -> str:
        raise NotImplementedError

    def get_memory_parser(self) -> Memory:
        raise NotImplementedError

    def get_read_package(
            self, filename: Path, precision: npy.floating
    ) -> ReadPackage:
        raise NotImplementedError

    def get_reader(self, filename: Path, precision:npy.floating) -> Reader:
        raise NotImplementedError

    def get_writer(self, filename: Path) -> Writer:
        raise NotImplementedError

    def get_read_test(self) -> ReadTest:
        raise NotImplementedError

    @property
    def supported_extensions(self) -> List[str]:
        raise NotImplementedError

    @property
    def supported_data_types(self) -> List[DataType]:
        raise NotImplementedError
