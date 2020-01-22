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

from pathlib import Path
from typing import List, Union

import numpy as npy
import pandas
import tables
from tqdm import tqdm

from PyPWA import info as _info
from PyPWA.libs.file.processor import ReaderBase
from . import _common, _unmanaged, _managed, _binning
from ... import vectors

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class BaseFolder(_common.CommonFolder):

    def __init__(self, file, folder):
        super(BaseFolder, self).__init__(file, folder)
        self.__create_folders()
        self.data = _managed._ModifyData(file, folder, len(self))
        self.binning = _binning._ManageBins(file, folder, self.root)
        self.unmanaged = _unmanaged._WriteUnManaged(file, folder, len(self))

    def __create_folders(self):
        if "unregulated" not in self._folder:
            self._file.create_group(self._folder, "unregulated")

        if "bin_folders" not in self._folder:
            self._file.create_group(self._folder, "bin_folders")


class ProjectDatabase:
    """Larger than memory data manipulation inside an HDF5 file
    Allows the user to operate on data larger than the systems RAM. This
    supports all data types, multiprocessing, and binning of ParticlePool
    data.
    Data is stored in the HDF5 using groups, or `folders`. Each file
    can have multiple different folders with different data and can be
    accessed independently from the other folders. Each folder has `root`
    data that must be either a ParticlePool or DataFrame, and then other
    types of data can be added along with the root data either as a
    `managed` data type that the table will `manage` for the user, or
    `unmanaged` where the user must ensure there will be no name conflicts
    or other issues.

    Parameters
    ----------
    file : str, Path
        The name of the HDF5 file, most commonly with a `hd5` extension
    mode : str
        Either 'a' or 'r' for append or read-only respectfully. If you
        try to open the table in write mode using 'w' it'll be changed to
        'a'ppend mode instead to avoid unintentionally overwriting data.
        Use path to delete the file if you wish to start fresh.

    See Also
    --------
    PyPWA.libs.binning, PyPWA.bin_by_range : For binning directly on an
        array or dataframe
    """

    def __init__(self, file: Union[Path, str], mode: str):

        # We only use Path for files, but pytables doesn't really support it
        file = str(file.absolute()) if isinstance(file, Path) else file

        # 'w' will overwrite all the data, everything.
        # This could be extremely destructive. Use Path(file).unlink() instead.
        mode = mode if mode != 'w' else 'a'

        compression = tables.Filters(
            complib="blosc", complevel=1, fletcher32=True
        )
        self.__file = tables.open_file(file, mode, filters=compression)

        if "pypwa" in self.__file.root:
            self.__group = self.__file.root.pypwa

        else:
            self.__group = self.__file.create_group(
                self.__file.root, "pypwa",
                title=f"v:0; Created with PyPWA {_info.VERSION}"
            )

    def __repr__(self):
        return (
            f"{__class__.__name__}"
            f"({self.__file.filename}, {self.__file.mode})"
        )

    def __len__(self):
        return len(self.__group._v_groups.keys())

    def __del__(self):
        self.close()

    def get_folder(self, name: str) -> BaseFolder:
        """Returns a base folder from the HDF5 file that was previously
        created.

        Parameters
        ----------
        name : str
            The name of the folder to parse from the

        Returns
        -------

        """
        try:
            return BaseFolder(self.__file, getattr(self.__group, name))
        except AttributeError:
            raise ValueError(f"{name} hasn't been created yet!")

    def make_folder(self, name: str,
                    data: Union[npy.ndarray, ReaderBase, vectors.ParticlePool],
                    filename: str, use_progress: bool = False,
                    desc: str = "") -> BaseFolder:
        try:
            folder = self.__file.create_group(self.__group, name)
            setup = _CreateRoot(self.__file, folder)
            setup.setup_root(data, use_progress, filename, desc)
            return BaseFolder(self.__file, folder)
        except tables.NodeError:
            raise FileExistsError("The project folder has already been made!")

    def remove_folder(self, name: str):
        try:
            folder = getattr(self.__file, name)
        except AttributeError:
            raise ValueError(f"No folder named {name}!")

        # Remove all the contents recursively
        self.__file.remove_node(folder, recursive=True)

    @property
    def folders(self) -> List[str]:
        return [folder for folder in self.__group._v_groups.keys()]

    def close(self):
        if self.__file.isopen:
            self.__file.flush()
            self.__file.close()


class _CreateRoot:
    # Forcing position is probably not needed here, but it ensures the dtype
    # will perfectly match everything else in PyPWA as well as GAMP
    class _PARTICLE(tables.IsDescription):
        x = tables.Float64Col(pos=0)
        y = tables.Float64Col(pos=1)
        z = tables.Float64Col(pos=2)
        e = tables.Float64Col(pos=3)

    def __init__(self, file: tables.File, folder: tables.Group):
        self.__file = file
        self.__folder = folder

    def setup_root(self,
                   data: Union[npy.ndarray, ReaderBase, vectors.ParticlePool],
                   use_progress: bool, filename: str, description: str):
        # tqdm has a disable flag, while we have an enable flag
        disable = not use_progress

        if isinstance(data, vectors.ParticlePool):
            length = data.event_count
        else:
            length = len(data)

        title = f"{length}:{filename}:{description}"

        if isinstance(data, ReaderBase):
            self.__reader_to_root_data(data, disable, title)

        elif isinstance(data, vectors.ParticlePool):
            self.__particle_pool_to_root(data, title)

        elif isinstance(data, npy.ndarray):
            self.__numpy_to_root(data, title)

        elif isinstance(data, pandas.DataFrame):
            self.__dataframe_to_root(data, title)

        else:
            raise ValueError(
                f"{type(data)} is an unsupported data type!"
            )

        self.__file.flush()

    def __reader_to_root_data(self, reader: ReaderBase, disable, desc):
        if reader.is_particle_pool:
            self.__parse_particle_pool(reader, disable, desc)
        else:
            self.__parse_regular_data(reader, disable, desc)

    def __parse_particle_pool(self, data: ReaderBase, disable: bool, desc):
        # Initialize the tables for the particles
        leaves = list()
        for index, the_id in enumerate(data.fields):
            leaves.append(
                self.__file.create_table(
                    where=self.__folder, name=f"root{index}_{the_id}",
                    description=self._PARTICLE, title=desc,
                    expectedrows=data.get_event_count()
                )
            )

        # Fill in data
        for event in tqdm(
                data, disable=disable, unit=" event", desc="Parsing root data",
                postfix=f"file={data.input_path.name}"):
            for p, leaf in zip(event.iter_particles(), leaves):
                leaf.row['x'] = p.x.to_numpy()
                leaf.row['y'] = p.y.to_numpy()
                leaf.row['z'] = p.z.to_numpy()
                leaf.row['e'] = p.e.to_numpy()
                leaf.row.append()

        for leaf in leaves:
            leaf.flush()

    def __parse_regular_data(self, data: ReaderBase, disable: bool, desc):
        # Create Table using the first event
        first = data.next()
        table = self.__file.create_table(
            where=self.__folder, name="root",
            description=first, expectedrows=data.get_event_count(),
            title=desc
        )

        row = self.__folder.root.row
        for event in tqdm(
                data, initial=1, disable=disable, unit=" event",
                postfix=f"file={data.input_path.name}",
                desc="Parsing root data"):
            for name in data.fields:
                row[name] = event[name]
            row.append()
        table.flush()

    def __particle_pool_to_root(self, data: vectors.ParticlePool, desc):
        for index, particle in enumerate(data.iter_particles()):
            table = self.__file.create_table(
                where=self.__folder, name=f"root{index}_{particle.id}",
                description=particle.data_frame, expectedrows=len(particle),
                title=desc
            )
            table.flush()

    def __numpy_to_root(self, array, desc):
        if len(array.dtype) > 0:
            table = self.__file.create_table(
                where=self.__folder, name="root",
                description=array, title=desc
            )
            table.flush()

        else:
            raise ValueError(
                "Numpy arrays must be structured to be root data!"
            )

    def __dataframe_to_root(self, df, desc):
        table = self.__file.create_table(
            where=self.__folder, name="root",
            description=df.to_records(index=False), title=desc
        )
        table.flush()
