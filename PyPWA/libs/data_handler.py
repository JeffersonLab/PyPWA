# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
