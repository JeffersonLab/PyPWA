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
************
File Package
************
This package handles reading and writing of all data inside PyPWA, from
GAMP files to HD5 tables. In this init file are all the functions, and
objects you'll need to quickly start loading and writing data with PyPWA.

Contained packages:
===================
- processor: This parses and writes files either one event at a time,
    or by the entire array
- project: This package handles reading and writing to a HD5 file in the
    PyPWA data structure. This handles multiple data types, predetermined
    data types, and unknown data types.
    This is also the package used for all binning in PyPWA.

Contained modules:
==================
- cache: This module handles caching data for reads and writes. It stores
    the sha512 sum of each file in the cache so that any changes to the
    original file can be caught and invalidate the cache. This is
    primarily used by `processor` but should be usable by anything.
- misc: This is a collection of useful functions that help the rest of
    the files work as intended. It provides the sha-sums, cache location,
    and file length for other modules in PyPWA
"""

from PyPWA import info as _info
from .project import ProjectDatabase
from .processor import DataProcessor as _Data, DataType

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


__all__ = [
    "ProjectDatabase",
    "get_reader", "get_writer", "read", "write"
]


def get_reader(filename: str):
    data = _Data(True, False)
    return data.get_reader(filename)


def get_writer(filename: str, dtype: DataType):
    data = _Data(True, False)
    return data.get_writer(filename, dtype)


def read(filename: str):
    data = _Data(True, False)
    return data.parse(filename)


def write(filename: str, data):
    writer = _Data(True, False)
    return writer.write(filename, data)
