"""
.. module:: pythonPWA.utilities
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various useful scripts.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy

def breitWigner(mass,resMass,gamma):
    """
    Briet Wigner function for a given mass, resonance mass, and resonance width.  Note that here, it assumes a fixed
    resonance width.

    Args:
    mass (float):
    resMass (float):
    gamma (float): 

    Returns:
    Numpy.complex value representing the Briet Wigner function value.
    """
    dr=mass-resMass
    denom=dr*dr+gamma*gamma/4.
    return numpy.complex(dr*gamma/(2.*denom),gamma*gamma/(denom*4.))