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
- processor: This parses and writes files either one event at a time
    through a reader or writer, or parses the entire file with a DataFrame
    through read or write.
- project: This package handles reading and writing to a HD5 file in the
    PyPWA data structure. This handles multiple data types, predetermined
    data types, and unknown data types.
    This is also the package used for binning with large amounts of data

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
from .processor import templates as _templates
from PyPWA.libs.vectors import ParticlePool as _pp
import numpy as _npy
import pandas as _pd
from typing import Union as _U

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


__all__ = [
    "ProjectDatabase",
    "get_reader", "get_writer", "read", "write"
]


def get_reader(filename: str, use_pandas=False) -> _templates.ReaderBase:
    """Returns a reader that can read the file one event at a time

    .. note::
        The return value from the reader coule bd a pointer, if you need
        to keep the event without it being overwrote on the next call, you
        must call the copy method on the returned data to get a unique
        copy.

    Parameters
    ----------
    filename : str, Path
        File to read
    use_pandas : bool
        Determines if a numpy data type or pandas data type is returned.

    Returns
    -------
    templates.ReaderBase
        A reader that can read the file, defined in PyPWA.plugins.data

    Raises
    ------
    RuntimeError
        If there is no plugin that can load the data found

    See Also
    --------
    read : Reads an entire file into a DataFrame, ParticlePool, or array

    Examples
    --------
    The reader can be used inside a standard `for` loop

    >>> reader = get_reader("example.gamp")
    >>> for event in reader:
    >>>     my_kept_event = event.copy()
    >>>     regular_event = event
    >>> reader.close()
    """
    data = _Data(True, False)
    return data.get_reader(filename, use_pandas)


def get_writer(filename: str, dtype: DataType) -> _templates.WriterBase:
    """Returns a writer that can write to the file one event at a time

    Parameters
    ----------
    filename : str, Path
        The file that you want to write to
    dtype : DataType
        Specifies the type of that needs to be written. TREE_VECTOR is
        used for ParticlePools and only works with the '.gamp' extension
        for now. STRUCTURED_ARRAY is used for both numpy structured arrays
        and pandas DataFrames. BASIC is used for standard numpy arrays.

    Returns
    -------
    templates.WriterBase
        A writer that can read the file, defined in PyPWA.plugins.data

    Raises
    ------
    RuntimeError
        If there is no plugin that can write the data found

    See Also
    --------
    write : Writes a ParticlePool, DataFrame, or array to file

    Examples
    --------
    The writer can be used to write a ParticlePool one event at a time

    >>> writer = get_writer("example.gamp", DataType.TREE_VECTOR)
    >>> for event in particles.iter_events():
    >>>     writer.write(event)
    >>> writer.close()
    """
    data = _Data(True, False)
    return data.get_writer(filename, dtype)


def read(
        filename: str, use_pandas=False, cache=True, clear_cache=False
) -> _U[_pd.DataFrame, _pp, _npy.ndarray]:
    """Reads the entire file and returns either DaataFrame, ParticlePool,
    or standard numpy array depending on the data found inside the file.

    Parameters
    ----------
    filename : Path, str
        File to read.
    use_pandas : bool
        Determines if a numpy data type or pandas data type is returned.
    cache : bool, optional
        Enables or disables caching. Defaults to the enabled. Leaving this
        enabled should do no harm unless there something is broken with
        caching. Disable this if returning the wrong data for debug
        purposes. If it continues to return the incorrect data when
        disabled then caching isn't the issue.
    clear_cache : bool, optional
        Forcefully clears the cache for the files that are parsed. Instead
        of loading the cache, it'll delete the cache and write a new cache
        object instead if cache is enabled.

    Returns
    -------
    DataFrame
        If the file is a kVars file, CSV, or TSV
    npy.ndarray
        If the file is a numpy file, PF file, or single column txt file
    ParticlePool
        If parsing a gamp file

    Raises
    ------
    RuntimeError
        If there is no plugin that can load the data found
    """
    data = _Data(cache, clear_cache)
    return data.parse(filename, use_pandas)


def write(filename: str, data, cache=True, clear_cache=False):
    """Reads the entire file and returns either DaataFrame, ParticlePool,
    or standard numpy array depending on the data found inside the file.

    Parameters
    ----------
    filename : Path, str
        The filename of the file you wish to write
    cache : bool, optional
        Enables or disables caching. Defaults to the enabled. Leaving this
        enabled should do no harm unless there something is broken with
        caching.
    clear_cache : bool, optional
        Forcefully clears the cache for the files that are parsed. It'll
        delete the cache and write a new cache object instead when cache
        is enabled.

    Raises
    ------
    RuntimeError
        If there is no plugin that can load the data found
    """
    writer = _Data(cache, clear_cache)
    return writer.write(filename, data)
