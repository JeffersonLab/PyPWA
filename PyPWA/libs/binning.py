#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2019 JLab
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

import json
import warnings
from collections import OrderedDict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

import numpy as npy
import tables

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.file import slot_table
from PyPWA.libs.file.processor import DataProcessor
from PyPWA.libs.math import reaction

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

"""
    
"""

_EVENT_CHUNK = 250000


class BinType(Enum):
    MASS = "mass"
    T_PRIME = "tp"
    T = "t"
    BEAM = "beam"


def make_bin_table(slot: slot_table.DataSlot):
    bin_types = [(name, "f8") for name in ["mass", "beam", "t", "tp"]]
    bin_array = npy.zeros(len(slot), bin_types)
    root = slot.get_root()

    # lower limit (ll), upper limit (ul)
    for ll in range(0, len(slot), _EVENT_CHUNK):
        ul = ll + _EVENT_CHUNK
        root_chunk = root.read(ll, ul)

        bin_array["mass"][ll:ul] = reaction.get_event_mass(root_chunk)
        bin_array["tp"][ll:ul] = reaction.get_t_prime(root_chunk)
        bin_array["t"][ll:ul] = reaction.get_t(root_chunk)
        bin_array["beam"][ll:ul] = root_chunk.get_particles_by_id(1)[0].z

    slot.add_data("bin_data", bin_array)
    slot.flush()


def bin_by_width(bins: npy.ndarray,
                 queue: OrderedDict,
                 position: int) -> Dict[str, npy.ndarray]:
    # Unpack queue
    upper = queue[position]["upper"]
    lower = queue[position]["lower"]
    count = queue[position]["count"]
    variable = queue[position]["variable"]

    # Size of each step in the standard data
    step_size = (upper - lower) / count
    truth_table = dict()

    # Handle events outside of the range
    truth_table["lower"] = bins[variable.value] < lower
    truth_table["upper"] = bins[variable.value] > upper

    step_with_count = enumerate(npy.arange(lower, upper, step_size))
    for index, lower_limit in step_with_count:
        x = bins[variable.value] > lower_limit
        y = bins[variable.value] < lower_limit + step_size
        truth_table[str(index)] = npy.logical_and(x, y)

    return truth_table


class _BinFixed:

    """
    .. Todo::
        This currently just splits the variable by length. This needs
        to be changed so that variables are ordered before they are
        binned.
    """

    def __init__(self, bins: npy.ndarray, queue: OrderedDict):
        self.__bins = bins
        self.__queue = queue
        self.__truth_table: npy.ndarray = None

        self.__reset()

    def __reset(self):
        self.__index = 0
        self.__list = []

    def get_fixed(
            self, position: int, truth_table: npy.ndarray = True
    ) -> List[npy.ndarray]:
        self.__reset()
        self.__truth_table = truth_table

        variable, fixed_size = self.__get_fixed_vars(position)
        lower, center, upper = self.__get_binning_information(fixed_size)

        self.__get_edge_events(lower)
        self.__get_center_events(upper, fixed_size)
        self.__get_edge_events(upper)
        return self.__list

    def __get_fixed_vars(self, position):
        val = self.__queue[position]
        return val["variable"], val["count"]

    def __get_binning_information(self, fixed_size):
        total = self.__truth_table.sum()
        num_in_center = total // fixed_size
        lower_extra = (total % fixed_size) // 2

        if (lower_extra * 2 + num_in_center * fixed_size) == total:
            upper_extra = lower_extra
        else:
            upper_extra = lower_extra + 1

        return lower_extra, num_in_center, upper_extra

    def __get_edge_events(self, limit):
        self.__list.append(self.__loop_until_limit(limit))

    def __get_center_events(self, center, fixed_size):
        for i in range(center):
            self.__list.append(self.__loop_until_limit(fixed_size))

    def __loop_until_limit(self, limit):
        count = 0
        while True:
            array = npy.zeros(len(self.__truth_table), bool)

            if self.__truth_table[self.__index]:
                count = count + 1
                array[self.__index] = True

            self.__index = self.__index + 1

            if count == limit:
                return array


class BinFactory:

    def __init__(self, slot: slot_table.DataSlot):
        self.__slot = slot
        if "bin_data" not in slot.extra_data:
            make_bin_table(slot)
        self.__bins = slot.get_data("bin_data").read()
        self.__queue = OrderedDict()
        self.__tree = dict()

        self.__fixed = _BinFixed(self.__bins, self.__queue)

    def add_fixed_range(
            self, variable: BinType, lower: int, upper: int, count: int):
        self.__queue[len(self.__queue)] = {
            "type": "width",
            "variable": variable,
            "lower": lower,
            "upper": upper,
            "count": count
        }

    def add_fixed_count(self, variable: BinType, count: int):
        self.__queue[len(self.__queue)] = {
            "type": "fixed",
            "variable": variable,
            "count": count
        }

    def clear(self):
        self.__queue.clear()

    def execute(self):
        self.__tree = self.__production_loop()

    def __production_loop(
            self, position: int = 0, previous: npy.ndarray = True
    ) -> Dict[int, npy.ndarray]:

        temp_storage = dict()
        truth_table_dict = self.__get_truth_tables(position, previous)

        for key, truth_table in truth_table_dict.items():
            if len(self.__queue) - 1 == position:
                temp_storage[key] = npy.logical_and(truth_table, previous)
            else:
                temp_storage[key] = self.__production_loop(
                    position + 1, truth_table
                )
        return truth_table_dict

    def __get_truth_tables(
            self, position, previous: npy.ndarray = True
    ) -> Dict[Any, npy.ndarray]:

        if not isinstance(previous, npy.ndarray):
            previous = npy.ones(len(self.__slot), bool)

        if self.__queue[position]["type"] == "width":
            return bin_by_width(self.__bins, self.__queue, position)
        else:
            # TODO: Actually implement this functionality
            raise NotImplementedError("Fixed bins are still a WIP")

    @property
    def produced_truth_table(self):
        return self.__tree


class BinSlot(slot_table.CustomSlot):

    def __init__(self, slot: slot_table.DataSlot):
        self.__file: tables.File = None
        self.__group: tables.Group = None
        self.__bin_group: tables.Group = None
        self.__data_group: tables.Group = None
        self.__data_slot = slot  # Data is slot is needed for names only
        warnings.simplefilter('ignore', tables.NaturalNameWarning)

    def setup_slot(self, file: tables.File, group: tables.Group):
        self.__file = file
        self.__group = group
        self.__data_group = getattr(
            file.root.data, self.__data_slot.group_name
        )

    def bin(self, truth_table: Dict[Any, npy.ndarray]):
        self.__make_bin_slot()
        metadata = self.__create_metadata(truth_table)
        self.__slot_to_bin(metadata, truth_table, self.__bin_group)
        self.__file.flush()
        self.__write_metadata(metadata)

    def __make_bin_slot(self):
        if self.__data_slot.group_name in self.__group._v_groups.keys():
            self.__file.remove_node(
                self.__group, self.__data_slot.group_name, True
            )

        self.__bin_group = self.__file.create_group(
            self.__group, self.__data_slot.group_name
        )

    def __create_metadata(self,
                          truth_table: Dict[Any, Any]) -> Dict[Any, Any]:
        metadata = dict()
        for leaf in truth_table.keys():
            if isinstance(truth_table[leaf], dict):
                metadata[leaf] = self.__create_metadata(truth_table[leaf])
            else:
                metadata[leaf] = {
                    "total": int(truth_table[leaf].sum())
                }
        return metadata

    def __slot_to_bin(self,
                      metadata: Dict[int, Any],
                      truth: Dict[int, Any],
                      current_group: tables.Group):
        for leaf in truth.keys():
            if isinstance(truth[leaf], dict):
                child = self.__file.create_group(current_group, str(leaf))
                self.__slot_to_bin(metadata[leaf], truth[leaf], child)
            else:
                child = self.__file.create_group(current_group, str(leaf))
                for array in self.__data_group._v_leaves.keys():
                    data = getattr(self.__data_group, array)
                    new_array = data.read_coordinates(truth[leaf])
                    if new_array.dtype.names:
                        self.__file.create_table(child, array, new_array)
                    else:
                        self.__file.create_array(child, array, new_array)

    def __write_metadata(self, metadata: Dict[int, Any]):
        file = self.__file.filename.strip(".h5")
        with open(file + "_bin_data.json", "w") as stream:
            json.dump(metadata, stream)

    def slot_to_folder(self):
        self.__write_out_data(
            Path("bin_folder"),
            getattr(self.__group, self.__data_slot.group_name)
        )

    def __write_out_data(self, current_folder, group):
        current_folder.mkdir()
        if group._v_groups.keys():
            for key in group._v_groups.keys():
                new_folder = current_folder / key
                new_group = getattr(group, key)
                self.__write_out_data(new_folder, new_group)
        else:
            dp = DataProcessor()
            slot = slot_table.DataSlot(self.__file, group)

            if slot.is_particle:
                dp.write(current_folder / "root.gamp", slot.get_root().read())
            else:
                dp.write(current_folder / "root.csv", slot.get_root().read())

            for extra in slot.extra_data:
                data = slot.get_data(extra).read()
                if data.dtype.names:
                    location = current_folder / (extra + ".csv")
                    dp.write(location, data)
                elif data.dtype == 'bool':
                    location = current_folder / (extra + ".pf")
                    dp.write(location, data)
                else:
                    location = current_folder / (extra + ".txt")
                    dp.write(location, data)

    @property
    def root_name(self):
        return "bin_slot"
