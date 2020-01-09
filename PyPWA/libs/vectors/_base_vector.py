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

import numpy as npy
import pandas as pd

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def sanitize_vector_input(x, y=None, z=None, e=None, has_e=False):
    try:
        df = pd.DataFrame(x)
    except Exception:
        df = None

    if isinstance(x, pd.Series):
        df = x

    if all(hasattr(df, col) for col in ["x", "y", "z"]):
        if has_e and hasattr(df, "e"):
            return df
        elif not has_e:
            try:
                return df.drop("e")
            except KeyError:
                return df

    elif all([isinstance(var, (int, float)) for var in [x, y, z]]):
        vector = pd.DataFrame()
        vector["x"] = npy.array([x])
        vector["y"] = npy.array([y])
        vector["z"] = npy.array([z])

        if has_e:
            if isinstance(e, type(None)):
                raise ValueError("No E value provided!")
            else:
                vector["e"] = npy.array([e])

        return vector

    elif all([hasattr(var, "__len__") for var in [x, y, z]]):
        df = pd.DataFrame()
        df["x"] = x
        df["y"] = y
        df["z"] = z
        if has_e:
            if hasattr(e, "__len__"):
                df["e"] = e
            else:
                raise ValueError("E not provided or wrong type!")
        return df

    elif isinstance(x, int):
        dtype = [("x", "f8"), ("y", "f8"), ("z", "f8")]
        if has_e:
            dtype.append(("e", "f8"))
        return pd.DataFrame(npy.zeros(x, dtype))

    else:
        raise ValueError("Can't sanitize vector input!")


class VectorMath:

    __slots__ = ["_vector"]

    def __init__(self, vector):
        self._vector = vector

    def get_length(self) -> Union[pd.Series, float]:
        return npy.sqrt(self.x**2 + self.y**2 + self.z**2)

    def get_theta(self) -> Union[pd.Series, float]:
        return npy.arccos(self.get_cos_theta())

    def get_phi(self) -> Union[pd.Series, float]:
        return npy.arctan2(self.y, self.x)

    def get_sin_theta(self) -> Union[pd.Series, float]:
        return (self.x**2 + self.y**2) / self.get_length()

    def get_cos_theta(self) -> Union[pd.Series, float]:
        return self.z / self.get_length()

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._vector

    @property
    def x(self) -> pd.Series:
        return self._vector['x'].copy()

    @x.setter
    def x(self, value: Union[npy.ndarray, float, pd.Series, str]):
        if isinstance(value, str):
            self._vector['x'] = npy.float64(value)
        else:
            self._vector['x'] = value

    @property
    def y(self) -> pd.Series:
        return self._vector['y'].copy()

    @y.setter
    def y(self, value: Union[npy.ndarray, float, pd.Series]):
        if isinstance(value, str):
            self._vector['y'] = npy.float64(value)
        else:
            self._vector['y'] = value

    @property
    def z(self) -> pd.Series:
        return self._vector['z'].copy()

    @z.setter
    def z(self, value: Union[npy.ndarray, float, pd.Series]):
        if isinstance(value, str):
            self._vector['z'] = npy.float64(value)
        else:
            self._vector['z'] = value
