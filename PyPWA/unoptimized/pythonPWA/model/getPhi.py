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


def get_phi(mass, resonance):
    """
    Returns the value of Phi used in complex production amplitude
    calculation, and thus number of _events (nTrue.nTrue()), for a
    specified mass and resonance. Invert Mass and Resonance to flip the
    function to arc-co-tan

    Args:
        mass (float):
        resonance (pythonPWA.dataTypes.resonance):

    Returns:
        Float representing the value of phi.
    """
    return numpy.arctan(
        (resonance.r0 * resonance.w0) / (mass**2 - resonance.w0**2)
    )