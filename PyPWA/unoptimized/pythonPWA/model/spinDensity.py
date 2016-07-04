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


class SpinDensity(object):

    @classmethod
    def calculate(cls, beam_polarization, α=None):
        if isinstance(α, type(None)):
            return cls._fixed_array()
        else:
            return cls._spin_density_calculation(beam_polarization, α)

    @staticmethod
    def _fixed_array():
        fixed_matrix = numpy.empty((2, 2), "c16")
        fixed_matrix[0, 0] = .5
        fixed_matrix[0, 1] = 0
        fixed_matrix[1, 0] = 0
        fixed_matrix[1, 1] = .5
        return fixed_matrix

    @staticmethod
    def _spin_density_calculation(beam_polarization, α):
        """
        SpinDensity matrix for specified beam polarization and angle
        alpha.

        Args:
            beam_polarization (float):
            α (float):

        Returns:
            The entire spinDensity matrix for specified beam polarization
            and angle alpha. Note that the spinDensity matrix is a 2x2
            matrix indexed by the wave reflectivity (wave.epsilon).
        """
        complex_ρ_matrix = numpy.empty((2, 2), 'c16')

        complex_ρ_matrix[0, 0] = numpy.complex(
            1. + beam_polarization * numpy.cos(2. * α), 0.
        )

        complex_ρ_matrix[0, 1] = numpy.complex(
            0., beam_polarization * numpy.sin(2. * α)
        )

        complex_ρ_matrix[1, 0] = numpy.complex(
            0., -1. * beam_polarization * numpy.sin(2. * α)
        )

        complex_ρ_matrix[1, 1] = numpy.complex(
            1. - beam_polarization * numpy.cos(2. * α), 0.
        )

        return .5 * complex_ρ_matrix