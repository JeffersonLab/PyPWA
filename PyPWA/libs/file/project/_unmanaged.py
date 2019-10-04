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

from typing import List, Tuple

import numpy as npy
import tables

from PyPWA import info as _info
from . import _common

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _ReadUnManaged:

    def __init__(self, file: tables.File, folder: tables.Group, length: int):
        self._file = file
        self._base_folder = folder
        self._length = length

        if "unregulated" in folder:
            self._extras = getattr(folder, "unregulated")
        else:
            self._extras = self._file.create_group(
                folder, "unregulated", title="Unmanaged data for PWA"
            )

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item) -> _common.StoredData:
        if isinstance(item, int):
            node = self.nodes[item][0]
            data = getattr(self._extras, node)

        # We want to strip out the length check and just check names
        elif item in [node[0] for node in self.nodes]:
            data = getattr(self._extras, item)

        else:
            raise KeyError(f"{item} is not a node name or index!")

        return _common.StoredData(data, data._v_title, len(data) == self._length)

    def get(self, node_name) -> _common.StoredData:
        data = getattr(self._extras, node_name)
        return _common.StoredData(data, data._v_title, len(data) == self._length)

    @property
    def nodes(self) -> List[Tuple[str, bool]]:
        nodes = []
        for leaf in self._extras._v_leaves.keys():
            node = getattr(self._extras, leaf)
            nodes.append((leaf, len(node) == self._length))
        return nodes


class _WriteUnManaged(_ReadUnManaged):

    def __init__(self, file: tables.File, folder: tables.Group, length: int):
        super(_WriteUnManaged, self).__init__(file, folder, length)

    def add(
            self, node_name: str, data: npy.ndarray, filename: str = "",
            description: str = "", ignore_length: bool = False):
        title = f"{len(data)}:{filename}:{description}"

        if not ignore_length:
            if len(data) != self._length:
                raise ValueError(
                    f"Data's length should be {self._length} not "
                    f"{len(data)}!"
                )

        if data.dtype.names:
            table = self._file.create_table(
                self._extras, node_name, data,
                title=title, expectedrows=len(data)
            )
        else:
            table = self._file.create_array(
                self._extras, node_name, data, title=title
            )

        table.flush()
