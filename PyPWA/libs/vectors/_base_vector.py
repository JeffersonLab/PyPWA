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
The backbone of all vectors
---------------------------
This provides the method for vector inputs to be sanitized into something
usable, and the base object for math that is similar for all vector types.
"""

from typing import Union, Tuple
from abc import abstractmethod

import numpy as np
import pandas as pd

from PyPWA.libs import common
from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def sanitize_vector_input(a, b=None, c=None, d=None, has_e=False):
    names = ["x", "y", "z"]
    if has_e:
        names.insert(0, "e")

    # Produce empty arrays of length X
    if isinstance(a, int) and isinstance(b, type(None)):
        if a == 0:
            if has_e:
                return np.float(0), np.float(0), np.float(0), np.float(0)
            return np.float(0), np.float(0), np.float(0)

        d = [np.zeros(a), np.zeros(a), np.zeros(a)]
        if has_e:
            d.append(np.zeros(a))
        return tuple(d)

    # Convert numpy storage types to contiguous arrays
    elif isinstance(a, (np.void, np.record)) or \
            isinstance(a, np.ndarray) and a.dtype.names:
        return common.to_contiguous(a, names)

    # Pass through single values
    elif all([isinstance(var, (int, float)) for var in [a, b, c]]):
        returns = [np.float(a), np.float(b), np.float(c)]
        if has_e:
            if not isinstance(d, (int, float)):
                raise ValueError("No Z value provided!")
            else:
                returns.append(np.float(d))
        return returns

    # Convert Structured Arrays to Contiguous Arrays
    elif all([isinstance(var, np.ndarray) for var in [a, b, c]]):
        if has_e:
            if not isinstance(d, np.ndarray):
                raise ValueError("No Z Value provided!")
            else:
                if all([d.flags["C_CONTIGUOUS"]] for d in [a, b, c, d]):
                    return a, b, c, d
                else:
                    return common.to_contiguous(
                        {"e": a, "x": b, "y": c, "z": d}, names
                    )
        else:
            if all([d.flags["C_CONTIGUOUS"]] for d in [a, b, c]):
                return a, b, c
            else:
                return common.to_contiguous({"x": a, "y": b, "z": c}, names)

    # Convert DataFrame to Contiguous Arrays
    elif isinstance(a, pd.DataFrame):
        return common.to_contiguous(a, names)

    # Pass the tuple from the records array directly
    elif isinstance(a, pd.Series):
        temp_storage = pd.DataFrame()
        temp_storage.append(a)
        return temp_storage.to_records(False)[0]

    else:
        raise ValueError(
            f"Can't sanitize vector input! Unknown data type {type(a)}!"
        )


class VectorMath:

    __slots__ = ["_x", "_y", "_z"]

    def __init__(self, x, y, z: np.ndarray):
        self._x = x
        self._y = y
        self._z = z

    def get_length(self) -> Union[pd.Series, float]:
        return np.sqrt(self._x**2 + self._y**2 + self._z**2)

    def get_theta(self) -> Union[pd.Series, float]:
        return np.arccos(self.get_cos_theta())

    def get_phi(self) -> Union[pd.Series, float]:
        return np.arctan2(self._y, self._x)

    def get_sin_theta(self) -> Union[pd.Series, float]:
        return (self._x**2 + self._y**2) / self.get_length()

    def get_cos_theta(self) -> Union[pd.Series, float]:
        return self._z / self.get_length()

    @property
    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({"x": self._x, "y": self._y, "z": self._z})

    @property
    def x(self) -> Union[float, np.ndarray]:
        if isinstance(self._x, np.ndarray):
            return self._x.copy()
        return self._x

    @x.setter
    def x(self, value: Union[np.ndarray, float, pd.Series, str]):
        if isinstance(value, np.ndarray):
            if len(value) != len(self._x):
                raise ValueError("Size does not match vector!")
            self._x = value
        else:
            self._x *= 0
            self._x += np.float64(value)

    @property
    def y(self) -> Union[float, np.ndarray]:
        if isinstance(self._y, np.ndarray):
            return self._y.copy()
        return self._y

    @y.setter
    def y(self, value: Union[np.ndarray, float, pd.Series]):
        if isinstance(value, np.ndarray):
            if len(value) != len(self._y):
                raise ValueError("Size does not match vector!")
            self._y = value
        else:
            self._y *= 0
            self._y += np.float64(value)

    @property
    def z(self) -> Union[float, np.ndarray]:
        if isinstance(self._z, np.ndarray):
            return self._z.copy()
        return self._z

    @z.setter
    def z(self, value: Union[np.ndarray, float, pd.Series]):
        if isinstance(value, np.ndarray):
            if len(value) != len(self._z):
                raise ValueError("Size does not match vector!")
            self._z = value
        else:
            self._z *= 0
            self._z += np.float64(value)
