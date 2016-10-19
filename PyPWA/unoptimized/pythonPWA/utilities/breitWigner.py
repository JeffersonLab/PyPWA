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


def breit_wigner_function(mass, resonance_mass, γ):
    """
    Briet Wigner function for a given mass, resonance mass, and resonance
    width.  Note that here, it assumes a fixed resonance width.

    Args:
        mass (numpy.float64):
        resonance_mass (numpy.float64):
        γ (numpy.float64):

    Returns:
        Numpy.complex value representing the Briet Wigner function value.
    """
    Δ_radius = mass - resonance_mass
    denominator = Δ_radius * Δ_radius + γ * γ / 4.

    real = Δ_radius * γ / (2. * denominator)
    imaginary = γ * γ / (denominator * 4.)

    return numpy.complex(real, imaginary)
