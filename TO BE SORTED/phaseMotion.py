"""
.. module:: pythonPWA
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various functions associated with calculating the phase motion between 2 waves.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>
"""

import numpy

def deltaPhi(v1,v2):
    return numpy.atan(numpy.imag(v1*numpy.conj(v2))/numpy.real(v1*numpy.conj(v2)))