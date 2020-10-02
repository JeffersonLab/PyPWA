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
Miscellaneous file tools.
-------------------------
"""

from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def pandas_to_numpy(df: Union[pd.Series, pd.DataFrame]) -> np.ndarray:
    """Converts Pandas DataTypes to Numpy

    Takes a Pandas Series or DataFrame and converts it to Numpy. Pandas
    does have a built in `to_records` function, however records are slower
    than Structured Arrays, while containing much of the same
    functionality.

    Parameters
    ----------
    df : Pandas Series or DataFrame
        The pandas data structure that you wish to be converted to
        standard Numpy Structured Arrays

    Returns
    -------
    Numpy ArrayLike
        The resulting Numpy array or structured array containing the data
        from the original DataFrame or Series. If it was a Series with
        each row named (like an element from a DataFrame) it'll be a
        Structured Array with length=1, if it was a standard Series it'll
        return a single Numpy Array, and if it was a DataFrame the results
        will be stored in Structured array matching the types and names
        from the DataFrame.
    """

    if isinstance(df, pd.Series) and isinstance(df.name, (type(None), str)):
        return df.to_numpy()

    names = list(df.keys())
    types = df.dtypes if len(df.dtypes) else [df.dtypes] * len(names)

    array_type = []
    for name, dtype in zip(names, types):
        array_type.append((name, dtype))

    if isinstance(df, pd.Series):
        length = 1
    else:
        length = len(df)

    array = np.empty(length, np.dtype(array_type, align=True))
    for name in names:
        array[name] = df[name]
    return array


def to_contiguous(
        data: Union[pd.DataFrame, np.ndarray, Dict[str, np.ndarray]],
        names: List[str]
) -> Union[np.ndarray, Tuple[np.ndarray, ...]]:
    """Convert DataFrame or Structured Array to List of Contiguous Arrays

    This takes a data-set and a list of column names and converts those
    columns into Contiguous arrays. The reason to use Contiguous arrays
    over DataFrames or Structured arrays is that the memory is better
    aligned to improve speed of computation. However, this does double
    the memory requirements of your data-set since this copies all the
    events over to the new array. Use only in amplitudes where you need
    to maximize the speed of your amplitude.

    Parameters
    ----------
    data : Structured Array, DataFrame, or Dict-like
        This is the data frame or Structured array that you want to
        extract columns from
    names : List of Column Names or str
        This is either a list of columns you want from the array, or a
        single column you want from the array

    Returns
    -------
    ArrayLike or Tuple[ArrayLike]
        If you provide only a single column, it'll only return a single
        array with the data from that array. However, if you have supplied
        multiple columns in a list or tuple, it'll return a tuple of
        arrays in the same order as the supplied names.
    """

    if isinstance(names, str):
        return np.ascontiguousarray(data[names])

    contiguous_data = []
    for name in names:
        try:
            contiguous_data.append(np.ascontiguousarray(data[name]))
        except IndexError:
            if isinstance(data, np.ndarray) and not data.dtype.names:
                raise ValueError(
                    f"to_contiguous doesn't support numpy flat arrays!"
                )
            else:
                raise ValueError(
                    f"to_contiguous doesn't support {type(data)}!"
                )

    return tuple(contiguous_data)
