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

import numpy as npy

from PyPWA import AUTHOR as _A, LICENSE as _L, VERSION as _V

__author__ = _A
__license__ = _L
__version__ = _V
__credits__ = ["Mark Jones", "Brandon Kaleiokalani", "Dr. Carlos Salgado"]


def helicity_spin_density(beam, alpha):
    spin = npy.empty((2, 2, len(alpha)), dtype=npy.complex)
    spin[0, 0] = npy.complex(1, 0)
    spin[1, 1] = npy.complex(1, 0)

    spin[0, 1] = -beam * npy.complex(npy.cos(-2 * alpha), npy.sin(-2 * alpha))
    spin[1, 0] = -beam * npy.complex(npy.cos(2 * alpha), npy.sin(2 * alpha))

    return spin / 2


def reflectivity_spin_density(beam, alpha):
    spin = npy.empty((2, 2, len(alpha)), dtype=npy.complex)

    spin[0, 0] = npy.complex(1 + beam * npy.cos(2 * alpha), 0)
    spin[0, 1] = npy.complex(0, beam + npy.sin(2 * alpha))
    spin[1, 0] = npy.complex(0, -beam * npy.sin(2 * alpha))
    spin[1, 1] = npy.complex(1 - beam * npy.cos(2 * alpha), 0)

    return spin / 2


def breit_wigner(mass, resonance_mass, resonance_width):
    delta_resonance = mass - resonance_mass
    denominator = delta_resonance**2 + resonance_width**2 / 4
    real = delta_resonance * resonance_width / (denominator * 2)
    imaginary = resonance_width**2 / (denominator * 4)
    return npy.complex(real, imaginary)
