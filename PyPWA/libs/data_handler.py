#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


def array_split(array, num_chunks):
    return numpy.array_split(array, num_chunks)


def dict_split(the_dict, num_chunks):
    """
    Splits dictionary into user defined number of chunks

    Args:
        the_dict (dict): Dictionary of arrays that needs to be split
        num_chunks (int): Number of chunks

    Returns:
        list: Each index is a chunk of the returned data in order
    """

    if num_chunks == 1:
        return [the_dict]

    split_dict = []

    for x in range(num_chunks):
        split_dict.append({})

    for data in the_dict:
        if isinstance(the_dict[data], numpy.ndarray):
            for index in range(num_chunks):
                split_dict[index][data] = numpy.array_split(
                    the_dict[data], num_chunks)[index]

        elif isinstance(the_dict[data], dict):
            for index in range(num_chunks):
                split_dict[index][data] = {}
            for key in the_dict[data]:
                for index in range(num_chunks):
                    split_dict[index][data][key] = numpy.array_split(
                        the_dict[data][key], num_chunks)[index]

    return split_dict
