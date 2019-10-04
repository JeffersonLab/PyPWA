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

import numpy as npy
import tables

from PyPWA import info as _info
from PyPWA.libs.file.processor import ReaderBase
from PyPWA.libs.math import vectors
from . import _common

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _ReadData:

    class Data(_Enum):
        QFACTOR = "qf"
        WEIGHTS = "weight"  # This used to be called bins in PyShell.
        WAVES = "wave"
        PASSFAIL = "pf"

    def __init__(self, file: tables.File, folder: tables.Group):
        self._file = file
        self._folder = folder

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item):
        if isinstance(item, int):
            node = self.nodes[item]
            data = getattr(self._folder, node)
        elif item in self.nodes:
            data = getattr(self._folder, item)
        else:
            raise KeyError(f"{item} not an index or in managed data!")

        return _common.StoredData(data, data._v_title)

    def __repr__(self):
        return (
            f"{__class__.__name__}("
            f"{_common._repr_table(self._file)}, "
            f"{self._folder._v_pathname})"
        )

    def get_data(self, data_type: Data,
                 node_id: int = -1) -> _common.StoredData:
        if node_id < 0:
            data = self._get_last_data_type(data_type)
        else:
            data = self._get_node_by_enum_and_id(data_type, node_id)

        return _common.StoredData(data, data._v_title)

    def _get_last_data_type(self, node_type: _Enum) -> _common.type_node:
        nodes = []
        for node in list(self._folder._v_children.keys()):
            if node_type.value in node:
                nodes.append(node)

        node = sorted(nodes)[-1]
        return getattr(self._folder, node)

    def _get_node_by_enum_and_id(self, node_type: _Enum,
                                 node_id: int) -> _common.type_node:
        search_key = f"{node_type.value}_{node_id}"
        for node in list(self._folder._v_leaves.keys()):
            if search_key in node:
                return getattr(self._folder, node)

        raise ValueError(f"No node with type {node_type} and id {node_id}!")

    @property
    def nodes(self):
        leaves = self._folder._v_leaves.keys()
        return [leaf for leaf in leaves if "root" not in leaf]


class _ModifyData(_ReadData):

    def __init__(self, file: tables.File, group: tables.Group, length: int):
        super(_ModifyData, self).__init__(file, group)
        self.__length = length

    def add_data(
            self, node_type: _ReadData.Data, data: npy.ndarray,
            filename: str = "", description: str = ""):

        self.__check_for_errors(data)
        data_name = self.__make_data_name(node_type)
        title = f"{len(data)}:{filename}:{description}"

        if isinstance(data, npy.ndarray):
            self.__add_array(data_name, data, title)

        elif isinstance(data, ReaderBase):
            self.__add_array_reader(data_name, data, title)

        else:
            raise ValueError(f"Unknown value type {type(data)}")

    def __check_for_errors(self, data):
        if isinstance(data, vectors.ParticlePool):
            raise ValueError("Particle data can only be root data!")

        if len(data) != self.__length:
            raise ValueError(
                f"Data has {len(data)} events, was expecting {self.__length}!"
            )

    def __make_data_name(self, node_type: _ReadData.Data):
        if isinstance(node_type, self.Data):
            return self.__get_new_id_name_for_enumeration(node_type)
        else:
            raise ValueError(f"{node_type!r} must be _ReadData.Data!")

    def __get_new_id_name_for_enumeration(self, dtype: _Enum) -> str:
        selected = []
        for node in self._folder._v_children.keys():
            if dtype.value in node:
                value = int(node.split("_")[1])
                selected.append(value)

        if len(selected):
            selected = sorted(selected)
        else:
            selected = [-1]

        return f"{dtype.value}_{selected[-1] + 1}"

    def __add_array(self, name: str, data: npy.ndarray, desc: str):
        if data.dtype.names:
            table = self._file.create_table(self._folder, name, data, desc)

        else:
            table = self._file.create_array(self._folder, name, data, desc)
        table.flush()

    def __add_array_reader(self, name: str, data: ReaderBase, desc: str):
        # Create an array that will hold all the data
        sample = data.next()
        data.reset()

        node = self._file.create_table(
            self._folder, name, sample.dtype, desc, expectedrows=len(data)
        )

        for event in data:
            row = node.row
            for name in sample.dtype.names:
                row[name] = event[name]
            row.append()
        node.flush()

    def replace_data(
            self, node_type: _ReadData.Data, node_id: int, data: npy.ndarray):

        self.__check_for_errors(data)
        description = ""  # Set to blank just in case

        # Figure out the real name of the data we're replacing
        if node_type in self.Data:
            name = f"{node_type.value}_{node_id}"

        else:
            raise ValueError(f"Uknown node type {node_type}")

        # Try to load the old description before deleting
        try:
            description = getattr(self._folder, name)._v_title
        except AttributeError:
            pass
        else:
            self._file.remove_node(self._folder, name)

        # Add the new data in its place
        self.add_data(node_type, data, description)

    def change_description(
            self, node_type: _ReadData.Data, the_id: int, desc: str):
        node = getattr(self._folder, f"{node_type.value}_{the_id}")
        node._v_title = desc
        self._file.flush()

    def delete(self, node_type: _ReadData.Data, node_id: int = -1):
        if node_type in self.Data:
            if node_id < 0:
                name = self._get_last_data_type(node_type)
            else:
                name = f"{node_type.value}_{node_id}"

        else:
            raise ValueError(f"Unknown node type {node_type}!")

        self._file.remove_node(self._file, name)
        self._file.flush()

    def delete_all(self, node_type: _ReadData.Data):
        for node in list(self._folder._v_leaves.keys()):
            if node_type.value in node:
                self._file.remove_node(self._folder, node)
