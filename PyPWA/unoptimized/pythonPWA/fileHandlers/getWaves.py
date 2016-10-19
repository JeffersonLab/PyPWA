#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import collections
import os

from PyPWA.unoptimized.pythonPWA import data_types
from PyPWA.unoptimized.pythonPWA.fileHandlers.bampReader import read_bamp
from PyPWA import LICENSE, STATUS, VERSION

__author__ = [
    "Brandon Kaleiokalani DeMello",
    "Joshua Pond",
    "Mark Jones"
]

__credits__ = [
    "Brandon Kaleiokalani DeMello",
    "Joshua Pond",
    "Mark Jones"
]

__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


class WaveFetch(object):

    def __init__(self, folder_path=False):
        if folder_path:
            self.new_path(folder_path)
        else:
            self._wave_deque = None  # type: collections.deque

    def new_path(self, folder_path):
        self._wave_deque = collections.deque()

        wave_files = self._fetch_wave_files(folder_path)

        for wave_file in wave_files:
            bamp_file = os.path.join(folder_path, wave_file)

            epsilon = self._fetch_epsilon_number(wave_file)
            wave_tuple_maker = data_types.Wave()
            self._wave_deque.append(
                wave_tuple_maker.make_wave(
                    epsilon,
                    read_bamp(bamp_file)
                )
            )

        return self.return_waves

    @staticmethod
    def _fetch_epsilon_number(file):
        wave_index = file.find(".bamp")
        string_epsilon = file[wave_index - 4]

        if string_epsilon == "+":
            epsilon = 0
        elif string_epsilon == "-":
            epsilon = 1
        else:
            raise IOError("Failed to find epsilon in {0}".format(file))

        return epsilon

    @staticmethod
    def _fetch_wave_files(folderpath):
        wave_list = []
        for file in os.listdir(folderpath):
            if ".bamp" in file:
                wave_list.append(file)

        return wave_list

    @property
    def return_waves(self):
        return self._wave_deque