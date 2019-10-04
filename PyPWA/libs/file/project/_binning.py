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

from __future__ import annotations

from enum import Enum as _Enum
from typing import Union

import numpy as npy
import tables
from tqdm import tqdm

from PyPWA import info as _info
from PyPWA.libs.math import reaction
from . import _common, _managed, _unmanaged

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _ManageBins:

    class BinVars(_Enum):
        MASS = "mass"
        T_PRIME = "tp"
        T = "t"
        BEAM = "beam"

    def __init__(self, file: tables.File, folder: tables.Group,
                 root: _common.StoredData):
        self.queue = dict()
        self.__file = file
        self.__data_folder = folder
        self.__root = root
        self.__event_description = f"{len(root)}:bin_events.pf:Sorting Array"
        self.__usable = True

        # We can only bin with ParticleLeaf
        if isinstance(self.__root.data, _common.ParticleLeaf):
            if "bin_data" in folder.unregulated:
                self.__bin_vars = getattr(folder.unregulated, "bin_data").read()
            else:
                self.__bin_vars = self.__make_bin_variable_table()
        else:
            self.__usable = False

    def __make_bin_variable_table(self):
        buffer = 25000
        bin_types = [(name, "f8") for name in ["mass", "beam", "t", "tp"]]
        bin_array = npy.zeros(len(self.__root), bin_types)

        # lower limit (ll), upper limit (ul)
        for ll in range(0, len(self.__root), buffer):
            ul = ll + buffer
            root_chunk = self.__root.data.read(ll, ul)

            bin_array["mass"][ll:ul] = reaction.get_event_mass(root_chunk)
            bin_array["tp"][ll:ul] = reaction.get_t_prime(root_chunk)
            bin_array["t"][ll:ul] = reaction.get_t(root_chunk)
            bin_array["beam"][ll:ul] = root_chunk.get_particles_by_id(1)[0].z

        table = self.__file.create_table(
            self.__data_folder.unregulated, "bin_data", bin_array,
            f"{len(bin_array)}:bin_data.csv:Binning Values",
            expectedrows=len(bin_array)
        )

        table.flush()
        return bin_array

    def __len__(self):
        """
        Returns the number of different bins there are inside the folder
        """
        return len(self.__data_folder.bin_folders._v_groups.keys())

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise IndexError("Only accepts integers")

        names = list(self.__data_folder.bin_folders._v_groups.keys())
        return _BinDirectory(
            self.__file, getattr(self.__data_folder.bin_folders, names[item])
        )

    def __repr__(self):
        return (
            f"{__class__.__name__}("
            f"{_common._repr_table(self.__file)},"
            f"{self.__data_folder._v_pathname}, {self.__root})"
        )

    def add_fixed_range(self, variable: BinVars, lower: int, upper: int,
                        count: int):
        if variable not in self.BinVars:
            raise ValueError("Variable must be a BinVariable!")

        self.queue[len(self.queue)] = (
            _CalculateWidths(
                self.__bin_vars[variable.value], lower,
                upper, count, self.__file
            )
        )

    def add_fixed_count(self, variable: BinVars, count: int):
        if variable not in self.BinVars:
            raise ValueError("Variable must be a BinVariable!")

        self.queue[len(self.queue)] = (
            _CalculateFixed(
                self.__bin_vars[variable.value], count, self.__file
            )
        )

    def clear(self):
        self.queue.clear()

    def execute(self, use_progress: bool = False):
        bin_folder = self.__get_new_bin_folder()

        executing_indices = tqdm(
            self.queue.keys(), disable=not use_progress
        )
        for index in executing_indices:
            first = index == 0
            self.__produce_sorting_arrays(self.queue[index], first, bin_folder)

        queue = []
        self.__make_data_copy_queue(bin_folder, queue)

        for copy in tqdm(queue, disable=not use_progress):
            copy.run()
        self.__file.flush()
        self.clear()

    def __get_new_bin_folder(self):
        selected = []
        for node in self.__data_folder.bin_folders._v_children.keys():
            value = node.split("_")[1]
            selected.append(int(value))

        selected = sorted(selected) if len(selected) else [-1]
        return self.__file.create_group(
            self.__data_folder.bin_folders, f"b_{(selected[-1] + 1)}"
        )

    def __produce_sorting_arrays(self, payload, first: bool,
                                 folder: tables.Group):
        if len(folder._v_groups):
            for child_name in folder._v_groups.keys():
                child_folder = getattr(folder, child_name)
                self.__produce_sorting_arrays(payload, first, child_folder)
        else:
            payload.run(folder, first)

    def __make_data_copy_queue(self, folder, processes):
        for child_name in folder._v_groups.keys():
            child_folder = getattr(folder, child_name)

            if hasattr(child_folder, "bin_events"):
                processes.append(
                    _CopyBinData(
                        self.__file, self.__data_folder,
                        child_folder, len(self.__bin_vars)
                    )
                )
            else:
                self.__make_data_copy_queue(child_folder, processes)

    def get_bin_directory(self, root_node=-1):
        if root_node < 0:
            folder = self.__get_last_bin_folder()
        else:
            folder = getattr(self.__data_folder.bin_folders, f"b_{root_node}")

        return _BinDirectory(self.__file, folder)

    def __get_last_bin_folder(self):
        nodes = []
        for node in list(self.__data_folder.bin_folders._v_children.keys()):
            nodes.append(node)

        return getattr(self.__data_folder.bin_folders, sorted(nodes)[-1])

    def remove_bin(self, bin_id: int):
        self.__file.remove_node(
            self.__data_folder.bin_folders, f"b_{bin_id}", recursive=True
        )

    def remove_all(self):
        self.__file.remove_node(
            self.__data_folder.bin_folders, recursive=True
        )
        self.__file.create_group(self.__data_folder, "bin_folders")
        self.__init__(self.__file, self.__data_folder, self.__root)

    @property
    def usable(self) -> bool:
        return self.__usable


class _CopyBinData:

    def __init__(self, file: tables.File, source_folder: tables.Group,
                 destination_folder: tables.Group, total_event_count: int):
        super(_CopyBinData, self).__init__()
        self.__file = file
        self.__source_folder = source_folder
        self.__destination_folder = destination_folder
        self.__selection_array = destination_folder.bin_events.read()
        self.__total_num_events = total_event_count

    def run(self):
        # Skip if this bin has no events
        if len(self.__selection_array) == 0:
            print("Bin created with no events!")
            self.__file.create_group(self.__destination_folder, "unregulated")
            return

        # Copy over the main data
        self.__iterate_over_folder(
            self.__source_folder, self.__destination_folder
        )

        # Copy over regular data
        unregulated = self.__file.create_group(
            self.__destination_folder, "unregulated"
        )
        self.__iterate_over_folder(
            self.__source_folder.unregulated, unregulated
        )

    def __iterate_over_folder(self, source_folder: tables.Group,
                              destination_folder: tables.Group):
        for node in source_folder._v_leaves.keys():
            source_node = getattr(source_folder, node)
            if len(source_node) == self.__total_num_events:
                self.__add_data_to_bin(source_node, destination_folder)

    def __add_data_to_bin(self, source_data: Union[tables.Array, tables.Table],
                          destination_folder: tables.Group):

        if isinstance(source_data, tables.Array):
            selected_data = source_data.read()[self.__selection_array]
            node = self.__file.create_array(
                destination_folder, source_data._v_name, selected_data,
                title=source_data._v_title
            )
        else:
            selected_data = source_data.read_coordinates(self.__selection_array)
            node = self.__file.create_table(
                destination_folder, source_data._v_name, selected_data,
                title=source_data._v_title, expectedrows=len(selected_data)
            )

        node.flush()


class _BinDirectory:

    def __init__(self, file, bin_folder):
        self.__file = file
        self.__bin_folder = bin_folder
        self.__all_folders = self.__generate_bin_folder_list()

    def __generate_bin_folder_list(self, this_folder=None, this_list=None):
        first = False
        if not this_folder:
            this_folder = self.__bin_folder
            this_list = []
            first = True

        for child_folder in this_folder._v_groups.keys():
            this_node = getattr(this_folder, child_folder)

            children_nodes = []
            for node in this_node._v_groups.keys():
                node = node.split("_")
                if node[0] == "f":
                    children_nodes.append("_".join(node))

            if not len(children_nodes):
                this_list.append(BinFolder(self.__file, this_node))
            else:
                self.__generate_bin_folder_list(this_node, this_list)

        if first:
            return this_list

    def __len__(self):
        return len(self.__all_folders)

    def __getitem__(self, item: Union[int, str]):
        try:
            item = int(item)
            return self.__all_folders[item]
        except ValueError:
            item = item.strip(self.__bin_folder._v_pathname)
            for folder in self.__all_folders:
                if folder.pathname == item:
                    return folder
            raise ValueError

    def delete(self):
        self.__file.remove_node(self.__bin_folder, recursive=True)


class _CalculateWidths:

    def __init__(self, array, lower, upper, count, file):
        self.__array = array
        self.__lower = lower
        self.__upper = upper
        self.__count = count
        self.__file = file
        self.__description = f"{len(array)}:bin_rejection.pf:"

    def run(self, base_group: tables.Group, first: bool):
        # Size of each step in the standard data
        step_size = (self.__upper - self.__lower) / self.__count
        selected = self.__get_selected(base_group, first)

        # Handle events outside of the range
        pass_fail = self.__array < self.__lower
        folder_select = self.__pass_fail_to_selected(pass_fail, selected)
        if len(folder_select):
            self.__make_bin_folder(base_group, "f_lower", folder_select)

        pass_fail = self.__array > self.__upper
        folder_select = self.__pass_fail_to_selected(pass_fail, selected)
        if len(folder_select):
            self.__make_bin_folder(base_group, "f_upper", folder_select)

        step_with_count = enumerate(
            npy.arange(self.__lower, self.__upper, step_size)
        )
        for index, lower_limit in step_with_count:
            x = self.__array > lower_limit
            y = self.__array < lower_limit + step_size
            pass_fail = npy.logical_and(x, y)
            folder_select = self.__pass_fail_to_selected(pass_fail, selected)
            self.__make_bin_folder(base_group, "f_%d" % index, folder_select)

        if not first:
            self.__file.remove_node(base_group.bin_events)

    def __get_selected(self, base_group: tables.Group, first: bool):
        if first:
            return npy.arange(0, len(self.__array), dtype="u4")
        else:
            return base_group.bin_events.read()

    def __make_bin_folder(self, base_group: tables.Group,
                          folder_name: str, selected: npy.ndarray):
        group = self.__file.create_group(base_group, folder_name)
        node = self.__file.create_array(
            group, "bin_events", selected, title=self.__description
        )
        node.flush()

    @staticmethod
    def __pass_fail_to_selected(pass_fail, selected):
        # Use the selected events to cut the pass_fail to size
        selected_pass_fail = pass_fail[selected]
        # Use the pass_fail to cut the selected events to the new selected
        return selected[selected_pass_fail]


class _CalculateFixed:

    def __init__(self, array: npy.ndarray, fixed_size: int, file: tables.File):
        self.__initial_array = array
        self.__sorting = array.argsort().argsort().astype("u4")
        self.__fixed_size = fixed_size
        self.__file = file
        self.__description = f"{len(array)}:bin_rejection.sel:"

    def __repr__(self):
        return "Fix this later "  # TODO ME

    def run(self, base_group: tables.Group, first: bool):
        sorted_select = self.__get_selected_events(base_group, first)
        num_in_center = len(sorted_select) // self.__fixed_size
        lower_cap = (len(sorted_select) % self.__fixed_size) // 2
        upper_cap = lower_cap + (num_in_center * self.__fixed_size)

        self.__create_bin_data(
            base_group, "f_lower", sorted_select[:lower_cap]
        )

        self.__create_bin_data(
            base_group, "f_upper", sorted_select[upper_cap:]
        )

        for index in range(num_in_center):
            lower_slice = lower_cap + (index * self.__fixed_size)
            upper_slice = lower_cap + (self.__fixed_size * (index + 1))
            self.__create_bin_data(
                base_group, "f_%d" % index,
                sorted_select[lower_slice:upper_slice]
            )

        # Clean up
        if not first:
            self.__file.remove_node(base_group.bin_events)

    def __create_bin_data(self, base_group, folder_name, array):
        group = self.__file.create_group(base_group, folder_name)
        node = self.__file.create_array(
            group, "bin_events", array, title=self.__description
        )
        node.flush()

    def __get_selected_events(self, base_group: tables.Group, first: bool):
        """
        Returns a selection array that's been sorted in the correct way

        .. warning::
            After you index the array, you **must** sort it again.

        :param base_group:
        :param first:
        :return:
        """
        if first:
            selected = npy.arange(0, len(self.__sorting), dtype="u4")
        else:
            selected = base_group.bin_events.read()

        # This cuts the sorting array into just the selected events
        sorting_array = self.__sorting[selected].argsort()
        # This then sorts the selected events by the sorting array
        array = selected[sorting_array]
        return array

    @staticmethod
    def __get_slice(array, lower, upper=-1):
        # Slices the array so that we only get the events we want
        print(len(array), lower, upper)
        if upper < 0:
            sliced = array[lower:]
        else:
            sliced = array[lower:upper]
        print(sliced)
        # Resorts the events so that they're back in order with the
        # original data. This is a must.
        return sliced


class BinFolder(_common.CommonFolder):

    def __init__(self, file, folder):
        super(BinFolder, self).__init__(file, folder)
        self.data = _managed._ReadData(file, folder)
        self.unmanaged = _unmanaged._ReadUnManaged(file, folder, len(self))

    @property
    def bin_location(self):
        location = self._folder._v_pathname.split('/')
        return '/'.join(location[5:])
