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
************************
Processes data for PyPWA
************************
This package reads and writes data for PyPWA in a variety of formats
defined by the plugins in PyPWA/plugins/data

.. seealso::
    ::mod:: `PyPWA.plugins.data`

Examples:
=========
 - To load data from file::
    data = DataProcessor()
    data.parse(path_to_file)
    reader = data.get_reader(path_to_file)

 - To write data to file::
    data = DataProcessor()
    data.write(path_to_file, the_data)
    writer = data.get_writer(path_to_file, DataType.BASIC)

Writer takes in DataType as an argument so that it can select which writer
to use depending on the type of data the user wants to write. You can
see what types are supported at :class:`PyPWA.libs.file.templates.DataType`.
"""

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION

from .main import DataProcessor, SUPPORTED_DATA, INPUT_TYPE
from .templates import DataType, ReaderBase, WriterBase
