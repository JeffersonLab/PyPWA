"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy
from PyPWA.unoptimized.pythonPWA.utilities import breitWigner


class ProductionAmplitude(object):
    """
    This is a recreation of the ProductionAmplitude class written by
    Dennis Weygand. The algorithmic structuring of this class is as
    similar to the ProductionAmplitude java version as possible.
    """
    def __init__(
            self, gList=[
                [0,0.],
                [1,.4],
                [2,1.],
                [3,0.],
                [4,0.],
                [5,0.],
                [6,0.],
                [7,0.],
                [8,0.]
            ]):

        self.g_list = gList

        self.GAMMA1 = numpy.float64(.340)
        self.MASS1 = numpy.float64(1.400)

        self.GAMMA2 = numpy.float64(.107)
        self.MASS2 = numpy.float64(1.320)

        self.MASS3 = numpy.float64(2.040)
        self.GAMMA3 = numpy.float64(.313)

        self.MASS4 = numpy.float64(1.720)
        self.GAMMA4 = numpy.float64(.135)

        self.MASS5 = numpy.float64(2.20)
        self.GAMMA5 = numpy.float64(.313)

        self.MASS_A1 = numpy.float64(1.230)
        self.WIDTH_A1 = numpy.float64(.360)

        self.MASS_PI2 = numpy.float64(1.672)
        self.WIDTH_PI2 = numpy.float64(.259)

        self.MASS_PI1 = numpy.float64(1.600)
        self.WIDTH_PI1 = numpy.float64(.350)

    def get_strength(self, beta):
        for g_pairs in self.g_list:
            if g_pairs[0] == beta:
                return g_pairs[1]

    def V(self, mass, beta, k, eps):
        g = self.get_strength(beta)

        if k < 1:
            if eps <= 1:
                return self._unnamed_function(mass, g, beta)

    def _unnamed_function(self, mass, g, beta):
        return {
            1: breitWigner.breit_wigner_function(
                mass, self.MASS1, self.GAMMA1) * g,

            2: breitWigner.breit_wigner_function(
                mass, self.MASS2, self.GAMMA2) * g,

            3: breitWigner.breit_wigner_function(
                mass, self.MASS3, self.GAMMA3) * g,

            4: breitWigner.breit_wigner_function(
                mass, self.MASS4, self.GAMMA4) * g,

            5: breitWigner.breit_wigner_function(
                mass, self.MASS5, self.GAMMA5) * g,

            6: breitWigner.breit_wigner_function(
                mass, self.MASS_A1, self.WIDTH_A1) * g,

            7: breitWigner.breit_wigner_function(
                mass, self.MASS_PI2, self.WIDTH_PI2) * g,

            8: breitWigner.breit_wigner_function(
                mass, self.MASS_PI1, self.WIDTH_PI1) * g
        }[beta]
