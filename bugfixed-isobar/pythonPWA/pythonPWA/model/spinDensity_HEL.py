"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy

def spinDensity(beampolarization,alpha):
    """
    SpinDensity matrix for specified beam polarization and angle alpha.

    Args:
    beampolarization (float):
    alpha (float):

    Returns:
    The entire spinDensity matrix for specified beam polarization and angle alpha.
    Note that the spinDensity matrix is a 2x2 matrix indexed by the wave reflectivity (wave.epsilon).
    """
    #TODO: need to make this check the type of alpha, if its type is none then return [[.5,0.],[0.,.5]]
    complexrhomatrix=numpy.empty((2,2),dtype=numpy.complex)
    complexrhomatrix[0,0]=numpy.complex(1.,0.)
    complexrhomatrix[0,1]=-1.*beampolarization*numpy.complex(numpy.cos(-2.*alpha),numpy.sin(-2.*alpha))
    complexrhomatrix[1,0]=-1.*beampolarization*numpy.complex(numpy.cos(2.*alpha),numpy.sin(2.*alpha))
    complexrhomatrix[1,1]=numpy.complex(1.,0.)
    return .5*complexrhomatrix
