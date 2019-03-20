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
This package reads and writes data for PyPWA.

Examples:
    To load data from file:
        data = DataProcessor()
        data.parse(path_to_file)
        reader = data.get_reader(path_to_file)
    To write data to file:
        data = DataProcessor()
        data.write(path_to_file, the_data)
        writer = data.get_writer(path_to_file, is_particle_pool, is_basic)

Writer two extra bools, is_particle_pool tells the writer to fetch a
writer that writes particle data, is_basic specifies an array that is
unstructured.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

from .file_processor import DataProcessor
from .data_templates import DataType, Reader, ReadPackage, Writer
