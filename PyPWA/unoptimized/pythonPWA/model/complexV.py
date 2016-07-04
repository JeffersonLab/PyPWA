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

from PyPWA.unoptimized.pythonPWA.model import magV
from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


def complexV(resonance, wave, waves, normalized_integral, mass):
    """
    Production amplitude (V) function.

    Args:
        resonance (pythonPWA.dataTypes.resonance):
        wave (pythonPWA.dataTypes.wave):
        waves (list)
        normalized_integral (pythonPWA.model.NormalizeIntegral):
        mass (float):

    Returns:
        A numpy.complex value representing a production amplitude.

    """


    magnitude = magV.magnitude_v(
        mass, resonance, wave, waves, normalized_integral
    )

    φ_cos = numpy.cos(
        model.getPhi(mass, resonance) + resonance.phase
    )

    φ_sin = numpy.sin(
        model.getPhi(mass, resonance) + resonance.phase
    )

    return numpy.complex(magnitude * φ_cos, magnitude * φ_sin)

