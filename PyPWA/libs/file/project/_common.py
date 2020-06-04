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

import dataclasses
import warnings
from typing import List, Tuple, Union, Dict

import numpy as npy
import tables
import yaml

from PyPWA import info as _info
from PyPWA.libs.file.processor import DataType
from PyPWA.libs import vectors

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class ParticleLeaf:
    """Functionally similar to Table for Particle Data

    The goal of ParticleLeaf is to provide a wrapper around the Tables
    for each Particle in a way that allows us to work with it in the same
    way that we'd work with a regular tables.Table. However, instead
    of it returning a numpy array, it'll return a ParticlePool containing
    each of the particles found in the table.

    Parameters
    ----------

    leaves
        List of the root particle tables. These are provided by
        :class:`Manage`.
    """

    # This object does not work with any other nodes other than root
    # nodes *that contain particle data.* That is data that has the
    # fields x, y, z, and e. Anything else will cause this object to
    # fail. Use pytables' builtin Table instead.

    def __init__(self, leaves: List[tables.Table]):
        self.__leaves = leaves
        self.__ids = [int(pid.name.split("_")[1]) for pid in leaves]

        particles = []
        for pid in self.__ids:
            particles.append(vectors.Particle(pid, 1))

        self.__pool = vectors.ParticlePool(particles)

    def __repr__(self):
        # leaves aren't the most repr friendly, so this cleans them up
        repr_leaves = [leaf._v_pathname for leaf in self.leaves]
        return f"{self.__class__.__name__}({repr_leaves})"

    def __len__(self):
        """
        Returns the number of events
        """
        return len(self.__leaves[0])

    def __getitem__(self,
                    item: Union[Tuple[int], List[int], slice, int]
                    ) -> vectors.ParticlePool:
        """Easily select your events in a pythonic way

        This allows you to cherry pick your events in much the same way
        you would with a numpy array.

        Use an integer to read a single event, provide a list of event
        indices, a PassFail array, or a slice to return a ParticlePool
        with the selected events.

        Examples
        --------

        ::

            event = particles[50]
            events = particles[50:15000:3]
            events = particles[[50,2500]]  # Only reads the 50 and 2500 events
            events = particles[[False, True, ..., False]]

        Which translates to::

            event = particles.read(50, 51)
            events = particles.read(start=50, stop=15000, step=3)
            events = particles.read_coordinates([50, 25000])
            events = particles.read_coordinates([False, True, ..., False])

        This allows for shorthand for both :meth:`ParticleLeaf.read` and
        :meth:`ParticleLeaf.read_coordinates`.

        """

        if isinstance(item, int):
            if item == len(self):
                raise IndexError
            return self.read(item, item + 1)

        elif isinstance(item, tuple) or isinstance(item, list):
            return self.read_coordinates(list(item))

        elif isinstance(item, slice):
            return self.read(item.start, item.stop, item.step)

        elif isinstance(item, npy.ndarray):
            return self.read_coordinates(item)

        else:
            raise AttributeError(f"Unknown type: {type(item)}")

    def read(self, start: int = 0, stop: int = None,
             step: int = None) -> vectors.ParticlePool:
        """Gets the particles from the group as a ParticlePool

        Start and stop only return values in the range of events, whereas
        step is how many events to skip. For a visual representation of
        what values are being selected see list(range(start, stop, step)).

        Examples
        --------

        Reading all particles::

            p.read()

        Reading the second event::

            p.read(1,2)
        """
        # If no options are provided, Table.read returns all data
        # If a single value is provided it'll read from that value to the end
        if not stop:
            values = [leaf.read(start) for leaf in self.__leaves]
            self.__replace_particle_pool(values)
            return self.__pool
        elif stop - start == 0:
            raise ValueError("Event size is zero!")

        values = [leaf.read(start, stop, step) for leaf in self.__leaves]

        # There is a harsh speed penalty on making objects, so instead
        # we just pump the values into existing objects if we can.
        if self.__pool.event_count == stop - start:
            self.__update_particle_pool(values)
        else:
            self.__replace_particle_pool(values)

        return self.__pool

    def read_coordinates(
            self, coords: Union[List[int], npy.ndarray]
    ) -> vectors.ParticlePool:
        """Get a set of events

        This allows you to select events either by using a lists of the
        indices that you want to read, or by passing an boolean array of
        the same length of the ParticleLeaf to select the events.
        """
        values = [leaf.read_coordinates(coords) for leaf in self.__leaves]

        try:
            self.__update_particle_pool(values)
        except ValueError:
            self.__replace_particle_pool(values)

        return self.__pool

    def __update_particle_pool(self, data: List[npy.ndarray]):
        for array, particle in zip(data, self.__pool.iter_particles()):
            particle.x = array["x"]
            particle.y = array["y"]
            particle.z = array["z"]
            particle.e = array["e"]

    def __replace_particle_pool(self, data: List[npy.ndarray]):
        ps = [vectors.Particle(pid, d) for pid, d in zip(self.__ids, data)]
        self.__pool = vectors.ParticlePool(ps)

    @property
    def leaves(self):
        # This prevents
        return [leaf for leaf in self.__leaves]


@dataclasses.dataclass
class StoredData:
    data: Union[tables.Table, ParticleLeaf]
    filename: str
    fixed_length: bool = True
    name: str = dataclasses.field(init=False)
    description: str = dataclasses.field(init=False)
    length: int = dataclasses.field(init=False)
    data_type: DataType = dataclasses.field(init=False)

    def __post_init__(self):
        self.length = len(self.data)
        try:
            self.description = self.filename.split(':')[2]
            self.filename = self.filename.split(':')[1]
        except IndexError:
            raise RuntimeError(f"{self.filename} is wrong!")

        # Store the name of the node
        if isinstance(self.data, ParticleLeaf):
            self.name = self.data.leaves[0]._v_name
        else:
            self.name = self.data._v_name

        # If we're using a writer, having the DataType already set
        # will make our lives easier
        if isinstance(self.data, ParticleLeaf):
            self.data_type = DataType.TREE_VECTOR
            extension = "gamp"
        elif isinstance(self.data, tables.Table):
            self.data_type = DataType.STRUCTURED
            extension = "csv"
        else:
            self.data_type = DataType.BASIC
            extension = "txt"

        # We want to make a filename if one doesn't exist already
        if not len(self.filename):
            self.filename = f"{self.name}.{extension}"

    def iterate_data(self, chunk_size: int = 250000) -> npy.ndarray:
        for lower in range(0, len(self.data), chunk_size):
            yield self.data.read(lower, lower + chunk_size)

    def __len__(self):
        return len(self.data)


"""
Types and Enumerations
"""

type_to_root = Union[npy.ndarray, vectors.ParticlePool]
type_root = Union[ParticleLeaf, tables.Table]
type_node = Union[tables.Group, tables.Table, tables.Array]

"""
Helping functions
"""


def _repr_table(table: tables.File) -> str:
    return f"tables.open_file({table.filename}, {table.mode})"


class CommonFolder:

    def __init__(self, file, folder):
        self._file = file
        self._folder = folder
        self._root = self.__load_root_data()

    def __load_root_data(self):
        # Load the root data
        all_names = self._folder._v_leaves.keys()
        roots = [name for name in all_names if "root" in name]

        # If only 1 root then we aren't working with particles
        if len(roots) == 1:
            data = getattr(self._folder, roots[0])
            return StoredData(data, data._v_title)

        # If more than 1, then we are working with particles
        # (Beam and Proton at least)
        elif len(roots) > 1:
            leaves = [getattr(self._folder, root) for root in roots]
            data = ParticleLeaf(leaves)
            return StoredData(data, leaves[0]._v_title)
        else:
            warnings.warn(
                f"{self._folder._v_pathname} has no root data!"
                f" Is this a bin with no events?"
            )

    def __len__(self):
        if self._root:
            return self._root.length
        else:
            return 0

    def __repr__(self):
        return (
            f"{__class__.__name__}"
            f"({_repr_table(self._file)}, {self._folder._v_pathname})"
        )

    def __str__(self):
        return f"{yaml.dump(self.info)}"

    @property
    def root(self) -> StoredData:
        return self._root

    @property
    def is_particle(self) -> bool:
        return isinstance(self._root, ParticleLeaf)

    @property
    def is_open(self) -> bool:
        return self._file.isopen

    @property
    def folder_name(self) -> str:
        return self._folder._v_name

    @property
    def pathname(self) -> str:
        return self._folder._v_pathname

    @property
    def info(self) -> Dict[str, Union[int, Dict[str, str]]]:
        if isinstance(self._root, type(None)):
            return dict()
        else:
            all_leaves = list(self._folder._v_leaves.keys())
            leaves = [x for x in all_leaves if x not in "root"]
            roots = [x for x in all_leaves if "root" in x]
            data = [x for x in leaves if x not in ["alphas", "bin_data"]]
            builtin = [x for x in leaves if x in ["alphas", "bin_data"]]

            if len(roots) == 1:
                roots = self._folder.root.dtype.names

            bin_folder = getattr(self._folder, "bin_folders")

            return {
                "roots": roots,
                "nodes": {
                    "data": data,
                    "builtin": builtin
                },
                "bin_count": len(bin_folder._v_groups.keys())
            }
