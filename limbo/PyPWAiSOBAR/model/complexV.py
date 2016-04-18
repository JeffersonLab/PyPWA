"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy
from PyPWAiSOBAR.model.magV import magV
from PyPWAiSOBAR.model.getPhi import getPhi

def complexV(resonance,wave,waves,normint,mass):
    """
    Production amplitude (V) function.

    Args:
    resonance (pythonPWA.dataTypes.resonance):
    wave (pythonPWA.dataTypes.wave):
    waves (list)
    normint (pythonPWA.model.normInt):
    mass (float):

    Returns:
    A numpy.complex value representing a production amplitude.

    """
    return numpy.complex(magV(mass,resonance,wave,waves,normint)*numpy.cos(getPhi(mass,resonance)+resonance.phase),magV(mass,resonance,wave,waves,normint)*numpy.sin(getPhi(mass,resonance)+resonance.phase))
    #return numpy.complex(magV(mass,resonance,wave,waves,normint)*(resonance.w0**2-mass**2)/(resonance.w0**2),magV(mass,resonance,wave,waves,normint)*(resonance.w0*resonance.r0)/(resonance.w0**2))