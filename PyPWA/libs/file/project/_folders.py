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

import warnings
from typing import Dict, Union

import yaml

from PyPWA import info as _info
from . import _common, _managed, _unmanaged, _binning

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


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
            return _common.StoredData(data, data._v_title)

        # If more than 1, then we are working with particles
        # (Beam and Proton at least)
        elif len(roots) > 1:
            leaves = [getattr(self._folder, root) for root in roots]
            data = _common.ParticleLeaf(leaves)
            return _common.StoredData(data, leaves[0]._v_title)
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
            f"({_common._repr_table(self._file)}, {self._folder._v_pathname})"
        )

    def __str__(self):
        return f"{yaml.dump(self.info)}"

    @property
    def root(self) -> _common.StoredData:
        return self._root

    @property
    def is_particle(self) -> bool:
        return isinstance(self._root, _common.ParticleLeaf)

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


class BaseFolder(CommonFolder):

    def __init__(self, file, folder):
        super(BaseFolder, self).__init__(file, folder)
        self.data = _managed._ModifyData(file, folder, len(self))
        self.binning = _binning._ManageBins(file, folder, self.root, len(self))
        self.unmanaged = _unmanaged._WriteUnManaged(file, folder, len(self))


class BinFolder(CommonFolder):

    def __init__(self, file, folder):
        super(BinFolder, self).__init__(file, folder)
        self.data = _managed._ReadData(file, folder)
        self.unmanaged = _unmanaged._ReadUnManaged(file, folder, len(self))

    @property
    def bin_location(self):
        location = self._folder._v_pathname.split('/')
        return '/'.join(location[5:])
