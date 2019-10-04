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

"""
****************
Project Database
****************
This package handles reading and writing from HD5 files in the PyPWA,
it supports multiple folders per file, larger than memory datasets,
binning, and more. This is the go-to package for any analysis containing
real data.

Example
=======
 - Start with opening a database and making your first folder::
    db = ProjectDatabase("dataset.hd5", "w")

    # We need the base data, checkout `processor` for how this works
    base_reader = get_reader("base_data.csv")
    db.makefolder("my important data", base_reader, "base_data.csv")
    important = db.get_folder("my important data")

 - Add some data to your database::
    important.data.add_data(DataTypes.QFactor, qfactor_data)
    important.unmanaged.add("unique_name", some_unique_data)

 - Read your data::
    x = important.data.read(DataTypes.QFactor)
    y = important.unmanaged.read("unique_name")

 - Bin your data::
    important.binning.add_fixed_count(BinVars.MASS, 1000)
    important.execute()

 - Walk over your freshly binned data::
    base_bin_directory = important.binning.get_bin_directory()
    for directory in base_bin_directory:
        directory.root.read()
        directory.data.read(DataTypes.QFactor)
        directory.unmanaged.read("unique_name")
"""

from PyPWA import info as _info
from ._binning import _ManageBins, BinFolder
from ._managed import _ReadData
from .main import ProjectDatabase, BaseFolder

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION

BinVars = _ManageBins.BinVars
DataTypes = _ReadData.Data
