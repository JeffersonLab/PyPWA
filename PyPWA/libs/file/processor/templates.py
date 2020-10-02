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
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

import pandas as pd
import numpy as np

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class DataType(enum.Enum):
    """
    Enumeration for type of data to be read or written using the reader
    and writer.

    Because of how the reader and writer are designed they can not
    inspect the data before it starts working with the data. This enum
    is used to specify the type of data you're working with.

    * BASIC = Standard arrays with no columns
    * STRUCTURED = Columned array (CSV, TSV, DataFrames)
    * TREE_VECTOR = Particle Data (GAMP)
    """

    # Single arrays with no attached data names
    BASIC = 0

    # Structured data, such as CSV or Evil data
    STRUCTURED = 1

    # Tree-like data. At this moment, only GAMP
    TREE_VECTOR = 2


class IMemory(ABC):

    @abstractmethod
    def parse(self, filename: Path) -> np.ndarray:
        ...

    @abstractmethod
    def write(self, filename: Path, data: Union[pd.DataFrame, np.ndarray]):
        ...


class ReaderBase(ABC):

    @abstractmethod
    def next(self) -> pd.DataFrame:
        """
        Called to get the next event from the reader.

        :return: A single event.
        :rtype: numpy.ndarray
        """
        ...

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

    @abstractmethod
    def get_event_count(self) -> int:
        """
        Called to get the total number of events in the file.

        :return: Count of the events
        :rtype: int
        """
        ...

    @abstractmethod
    def reset(self):
        """
        Resets the reader back to the first event
        """
        ...

    @abstractmethod
    def close(self):
        """
        Should close any open objects or streams.
        """
        ...

    @property
    def is_particle_pool(self) -> bool:
        return False

    @property
    @abstractmethod
    def fields(self) -> List[str]:
        ...

    @property
    @abstractmethod
    def data_type(self) -> DataType:
        ...

    @property
    @abstractmethod
    def input_path(self) -> Path:
        ...


class WriterBase(ABC):

    @abstractmethod
    def write(self, data: Union[pd.DataFrame, np.ndarray]):
        """
        Should write the received event to the stream.

        :param numpy.ndarray data: The event data stored in a numpy array.
        """
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @abstractmethod
    def close(self):
        """
        Should close the stream and any open streams or objects.
        """
        ...

    @property
    @abstractmethod
    def output_path(self) -> Path:
        ...


class IReadTest(ABC):

    @abstractmethod
    def can_read(self, filename: Path) -> bool:
        ...


class IDataPlugin:

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        ...

    @abstractmethod
    def get_memory_parser(self) -> IMemory:
        ...

    @abstractmethod
    def get_reader(self, filename: Path, use_pandas: bool) -> ReaderBase:
        ...

    @abstractmethod
    def get_writer(self, filename: Path) -> WriterBase:
        ...

    @abstractmethod
    def get_read_test(self) -> IReadTest:
        ...

    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        ...

    @property
    @abstractmethod
    def supported_data_types(self) -> List[DataType]:
        ...

    @property
    def use_caching(self) -> bool:
        return True

    @property
    def supports_iterators(self) -> bool:
        return True
