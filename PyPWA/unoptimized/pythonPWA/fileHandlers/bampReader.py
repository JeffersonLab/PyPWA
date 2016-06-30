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

from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


def read_bamp(filename):
    """
    This is a general bamp reading function.

    Args:
    filename (string): Path to bamp file to be read.

    Returns:
    List of numpy.complexes representing the complex amplitudes of the
    wave represented by the file.
    """
    temp1 = numpy.fromfile(file=filename,dtype=numpy.dtype('f8'))
    temp2 = temp1.reshape((2,-1),order='F')
    temp3 = []
    for lineNumber in range(temp2.shape[1]):
        temp3.append(numpy.complex(
            temp2[0, lineNumber],
            temp2[1, lineNumber]
        ))

    return temp3
