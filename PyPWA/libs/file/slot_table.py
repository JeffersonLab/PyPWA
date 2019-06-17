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
from typing import List, Union

import numpy as npy
import tables

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.math import vectors
from abc import ABC, abstractmethod

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

"""
... note:
    These objects break the rule of each class having it's own defined 
    __repr__, the reason for this is that pytables does not honor the
    eval(repr(obj)) rule, and instead pollutes it's repr with useless data.
"""


root_type = Union[npy.ndarray, vectors.ParticlePool]


def iter_root(
        root: Union["ParticleLeaf", tables.Table],
        chunk_size: int = 5000) -> npy.ndarray:

    for lower in range(0, len(root), chunk_size):
        yield root.read(lower, lower + chunk_size)


class _Particle(tables.IsDescription):
    x = tables.Float64Col()
    y = tables.Float64Col()
    z = tables.Float64Col()
    e = tables.Float64Col()


class ParticleLeaf:

    def __init__(self, leaves: List[tables.Table]):
        self.__leaves = leaves
        self.__ids = [int(pid.name.split("_")[2]) for pid in leaves]
        self.__pool = self.__create_empty_particle_pool()

    def __create_empty_particle_pool(self):
        particles = [vectors.Particle(pid, 0) for pid in self.__ids]
        return vectors.ParticlePool(particles)

    def __len__(self):
        return len(self.__leaves[0])

    def read(self, start: int = 0, stop: int = None) -> vectors.ParticlePool:
        if not stop:
            values = [leaf.read() for leaf in self.__leaves]
            self.__replace_particle_pool(values)
            return self.__pool

        values = self.__get_values(start, stop)
        if (stop - start) == self.__pool.event_count and stop < len(self):
            self.__update_particle_pool(values)
        else:
            self.__replace_particle_pool(values)
        return self.__pool

    def __get_values(self, start, stop) -> List[npy.ndarray]:
        return [leaf.read(start, stop) for leaf in self.__leaves]

    def __update_particle_pool(self, data: List[npy.ndarray]):
        for array, particle in zip(data, self.__pool.iter_particles()):
            particle.e = array["e"]
            particle.x = array["x"]
            particle.y = array["y"]
            particle.z = array["z"]

    def __replace_particle_pool(self, data: List[npy.ndarray]):
        ps = [vectors.Particle(pid, d) for pid, d in zip(self.__ids, data)]
        self.__pool = vectors.ParticlePool(ps)

    @property
    def leaves(self):
        return self.__leaves
        

class DataSlot:

    def __init__(self, file: tables.File, group: tables.Group):
        self.__file = file
        self.__group = group

        self.__root = self.__load_root()
        self.__event_count = len(self.__root)

    def __load_root(self) -> Union[tables.Table, ParticleLeaf]:
        roots = self.__get_root_names()
        if len(roots) == 1:
            return getattr(self.__group, roots[0])

        elif len(roots) > 1:
            leaves = [getattr(self.__group, root) for root in roots]
            return ParticleLeaf(leaves)

        else:
            raise ValueError(f"{self.__group._v_name} has no root data!")

    def __get_root_names(self) -> List[str]:
        data_names = self.__group._v_leaves.keys()
        return [name for name in data_names if "root" in name]

    def __len__(self):
        return len(self.__root)

    def get_root(self)-> Union[tables.Table, ParticleLeaf]:
        return self.__root

    def add_data(self, name: str, data: npy.ndarray = None):
        self.__check_array_length(data)
        if data.dtype.names:
            self.__file.create_table(self.__group, name, data)
        else:
            self.__file.create_array(self.__group, name, data)
        self.__file.flush()

    def __check_array_length(self, data: npy.ndarray):
        if len(self) != len(data):
            raise IndexError(
                f"Data supplied is the wrong size!"
                f" Must have {len(self)} rows to fit!"
            )

    def get_data(self, name: str) -> tables.Array:
        self.__check_data_for_name(name)
        return getattr(self.__group, name)

    def remove_data(self, name: str):
        self.__check_data_for_name(name)
        self.__file.remove_node(self.__group, name)
        self.__data_names = list(self.__group._v_leaves.keys())

    def __check_data_for_name(self, name: str):
        if name not in self.extra_data:
            raise ValueError(f"{name} not in slot!")

    def root_append(self, data: root_type):
        if isinstance(data, vectors.ParticlePool):
            self.__append_particle_data(data)

        elif isinstance(data, npy.ndarray):
            self.__append_table_data(data)
        
        else:
            raise ValueError(
                "Root Data must be a structured array or ParticlePool!"
            )

    def __append_particle_data(self, data: vectors.ParticlePool):
        for event in data.iter_events():
            for p, leaf in zip(event.iter_particles(), self.__root.leaves):
                row = leaf.row
                row["x"] = p.x
                row["y"] = p.y
                row["z"] = p.z
                row["e"] = p.e
                row.append()

    def __append_table_data(self, data: npy.ndarray):
        for event in data:
            row = self.__root.row
            for name in data.dtype.names:
                row[name] = event[name]
            row.append()

    def flush(self):
        self.__file.flush()

    @property
    def extra_data(self) -> List[str]:
        return [l for l in self.__group._v_leaves.keys() if "root" not in l]

    @property
    def is_particle(self) -> bool:
        return isinstance(self.__root, ParticleLeaf)

    @property
    def group_name(self) -> str:
        return self.__group._v_name


class CustomSlot(ABC):

    @abstractmethod
    def setup_slot(self, file: tables.File, group: tables.Group):
        ...

    @property
    @abstractmethod
    def root_name(self) -> str:
        ...


class SlotFactory:

    def __init__(self, file: Union[Path, str], mode: str):
        file = str(file.absolute()) if isinstance(file, Path) else file
        mode = mode if mode != 'w' else 'a'  # We really don't want 'w'

        self.__file = tables.open_file(file, mode)
        if "data" in self.__file.root:
            self.__group = self.__file.root.data
        else:
            self.__group = self.__file.create_group(self.__file.root, "data")

    def __del__(self):
        self.close()

    def add_slot(self, name: str,
                 fields: List[str],
                 is_particle: bool = False,
                 length: int = 100000):
        new_slot = self.__file.create_group(self.__group, name)
        if is_particle:
            self.__make_multiple(new_slot, fields, length)
        else:
            self.__make_single(new_slot, fields, length)
        self.__file.flush()

    def __make_multiple(self,
                        slot: tables.Group,
                        ids: List[str],
                        length: int):
        for index, the_id in enumerate(ids):
            name = "root_p" + str(index) + "_" + str(the_id)
            self.__file.create_table(
                slot, name, _Particle, expectedrows=length
            )

    def __make_single(self, slot: tables.Group, ids: List[str], length: int):
        data_type = [(name, "f8") for name in ids]
        self.__file.create_table(
            slot, "root", npy.zeros(0, data_type), expectedrows=length
        )

    def remove_slot(self, name: str):
        slot = getattr(self.__group, name)
        self.__file.remove_node(self.__file, slot)
        self.__file.flush()

    def get_slot(self, name: str):
        if name in self.slots:
            slot = getattr(self.__group, name)
            return DataSlot(self.__file, slot)
        else:
            raise ValueError(f"{name} isn't in dataset!")

    def set_custom_slot(self, custom: CustomSlot):
        if custom.root_name in self.__file.root._v_groups.keys():
            slot = getattr(self.__file.root, custom.root_name)
        else:
            slot = self.__file.create_group(self.__file.root, custom.root_name)
        custom.setup_slot(self.__file, slot)

    @property
    def slots(self) -> List[str]:
        return self.__group._v_groups.keys()

    def close(self):
        if self.__file.isopen:
            self.__file.flush()
            self.__file.close()
