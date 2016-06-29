"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy
from PyPWA.unoptimized.pythonPWA.utilities.breitWigner import breitWigner

def magV(mass,resonance,wave,waves,normint):
    """
    Returns the magnitude of the production amplitued V, for a specified wave, 
    resonance, wave in the set of waves, and normalization integral.
    """
    return numpy.sqrt((1./normint[wave.epsilon,wave.epsilon,waves.index(wave),waves.index(wave)])*resonance.wR[waves.index(wave)]*resonance.cR*breitWigner(mass,resonance.w0,resonance.r0)*numpy.conjugate(breitWigner(mass,resonance.w0,resonance.r0)))