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

import collections

from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


class Resonance(object):
    """
    This class represents a resonance.
    """
    def __init__(self):
        self._master_resonance = collections.namedtuple(
            "Resonance", ["cR", "wR", "w0", "r0", "phase"]
        )

    def make_resonance(self, cR, wR, w0, r0, phase):
        return self._master_resonance(
            cR, wR,
            w0, r0,
            phase
        )


class Wave(object):
    """
    This class represents a PWA wave.
    """
    def __init__(self):
        self._master_wave = collections.namedtuple(
            "Wave",
            ["epsilon", "complex_amplitudes", "beta", "k", "filename"]
        )

    def make_wave(self, epsilon, complex_amplitudes, beta, k, filename):
        return self._master_wave(
            epsilon, complex_amplitudes,
            beta, k,
            filename
        )
