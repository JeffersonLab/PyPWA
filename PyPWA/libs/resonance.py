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

from pathlib import Path
from typing import Union, List, Optional as Opt

import pandas as pd


class _Resonance:

    def __init__(self, row_segment: pd.Series):
        self.__segment = row_segment

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"res({repr(self.__segment)}"

    @property
    def Cr(self) -> float:
        return self.__segment["Cr"]

    @Cr.setter
    def Cr(self, value: float):
        self.__segment["Cr"] = value

    @property
    def W0(self) -> float:
        return self.__segment["W0"]

    @W0.setter
    def W0(self, value: float):
        self.__segment["W0"] = value

    @property
    def R0(self) -> float:
        return self.__segment["R0"]

    @R0.setter
    def R0(self, value: float):
        self.__segment["R0"] = value

    @property
    def waves(self) -> pd.Series:
        return self.__segment[3:]

    @waves.setter
    def waves(self, values: List[float]):
        if len(values) == len(self.waves):
            for index, value in enumerate(values):
                self.__segment[f"Wave{index}"] = value


class _Waves:

    def __init__(self, row_segment):
        self.__segment = row_segment

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"wave({repr(self.__segment)}"

    @property
    def E(self) -> int:
        return self.__segment["E"]

    @E.setter
    def E(self, value: int):
        self.__segment["E"] = value

    @property
    def L(self) -> int:
        return self.__segment["L"]

    @L.setter
    def L(self, value: int):
        self.__segment["L"] = value

    @property
    def M(self) -> int:
        return self.__segment["M"]

    @M.setter
    def M(self, value: int):
        self.__segment["M"] = value


class ResonanceData:

    def __init__(self, file: Opt[Union[Path, str]] = False):
        if file:
            self.__elm = pd.read_excel(file, "elm", index_col="wave")
            self.__resonance = pd.read_excel(file, "resonance")
        else:
            self.__elm = pd.DataFrame(columns=["E", "L", "M"], dtype=int)
            self.__resonance = pd.DataFrame(columns=["Cr", "W0", "R0"])

    def add_resonance(self, cr, w0, r0):
        new_data = {"Cr": cr, "W0": w0, "R0": r0}
        for index in range(len(self.__resonance.columns) - 3):
            new_data[f"Wave{index}"] = 0

        self.__resonance = self.__resonance.append(new_data, ignore_index=True)
        return _Resonance(self.__resonance.iloc[-1])

    def add_wave(self, e: int, l: int, m: int):
        indexes = sorted([int(name.strip("wave")) for name in self.__elm.index])
        index = indexes[-1] + 1

        wave_data = pd.Series({"E": e, "L": l, "M": m})
        wave_data.name = f"wave{index}"

        self.__resonance[f"Wave{index}"] = 0
        self.__elm = self.__elm.append(wave_data)

    def get_resonance(self, index) -> _Resonance:
        return _Resonance(self.__resonance.loc[index])

    def get_wave(self, index) -> _Waves:
        return _Waves(self.__elm.loc[f"wave{index}"])

    def remove_resonance(self, index):
        self.__resonance = self.__resonance.drop(index)
        self.__resonance = self.__resonance.reset_index(drop=True)

    def remove_wave(self, index):
        self.__elm = self.__elm.drop(f"wave{index}")
        self.__resonance = self.__resonance.drop(f"Wave{index}", axis=1)

    @property
    def elm_dataframe(self) -> pd.DataFrame:
        return self.__elm.copy()

    @property
    def resonance_dataframe(self) -> pd.DataFrame:
        return self.__resonance.copy()

    @property
    def res_index(self):
        return len(self.__resonance)

    @property
    def wave_index(self):
        return len(self.__elm)

    def save(self, file: Union[Path, str]):
        writer = pd.ExcelWriter(file)
        self.__resonance.to_excel(writer, "resonance", index=False)
        self.__elm.to_excel(writer, "elm", index_label="wave")
        writer.save()
