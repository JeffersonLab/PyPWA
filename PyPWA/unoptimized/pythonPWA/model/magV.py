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

from PyPWA.unoptimized.pythonPWA.utilities.breitWigner import \
    breit_wigner_function
from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


def magnitude_v(mass, resonance, wave, waves, normalized_integral):
    """
    Returns the magnitude of the production amplitude V, for a specified
    wave, resonance, wave in the set of waves, and normalization integral.
    """

    breit_wigner_solution = breit_wigner_function(
        mass, resonance.w0, resonance.r0
    )

    integral_solution = 1. / normalized_integral[
        wave.epsilon,
        wave.epsilon,
        waves.index(wave),
        waves.index(wave)
    ]

    final_solution = numpy.sqrt(
        integral_solution * resonance.wR[waves.index(wave)] *
        resonance.cR * breit_wigner_solution *
        numpy.conjugate(breit_wigner_solution)
    )

    return final_solution