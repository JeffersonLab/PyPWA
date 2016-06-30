"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>
"""
import numpy

def getPhi(mass,resonance):
    """
    Returns the value of Phi used in complex production amplitude calculation, and thus
    number of _events (nTrue.nTrue()), for a specified mass and resonance.
    
    Args:
    mass (float):
    resonance (pythonPWA.dataTypes.resonance):

    Returns:
    Float representing the value of phi.
    """
    return numpy.arctan((resonance.r0*resonance.w0)/(mass**2-resonance.w0**2)) #need to make this arccotan? invert args