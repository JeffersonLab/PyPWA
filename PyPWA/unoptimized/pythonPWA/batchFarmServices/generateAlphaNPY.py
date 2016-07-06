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

import os
import sys

import numpy

from PyPWA.unoptimized.pythonPWA.utilities import vectors
from PyPWA.libs.data.builtin import gamp
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones", "Stephanie K. A. Bramlett", "Joshua Pond"]
__credit__ = ["Mark Jones", "Stephanie K. A. Bramlett", "Joshua Pond"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


class GenerateAlphas(object):
    alphaName = "alpha"
    labelOut = ""

    def __init__(self, mode, indir, gfile):
        """
        This program calculates the value of alpha for every event in a
        .gamp file and saves it to a .txt list, one event per line.

        Args:
            mode (int):  8 = p pi+ pi- pi0, 22 = p p+ p-, 24 = p k+ k-,
                42 = gamma p --> p Ks Ks (pi+ pi- pi+ pi-)
            indir (string): Full file path to directory of file
            gfile (string): File name without .gamp extension.
        """

        self.mode = mode
        self.indir = indir
        self.gfile = gfile + ".gamp"
        self.nfile = gfile + ".npy"
        f = gfile.partition(".")[0]
        self.gampT = gamp.GampMemory()
        self.gampList = self.gampT.parse(os.path.join(self.indir + self.gfile))
        self.alphaName = "alpha" + f + ".txt"
        self.alphalist = []
        if self.mode == "8":
            self.analyze8()
        if self.mode == "22":
            self.analyze22()
        if self.mode == "24" or self.mode == 24 :
            self.analyze24()
        if self.mode == "42":
            self.analyze42()
        if self.mode == "EtaPiN":
            self.analyzeEtaPiN

    def analyze8(self):
        """
        p pi+ pi- pi0
        """
        for event in self.gampList:
            for particles in event:
                if particles[0] == 14.0:  # proton
                    p = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )
                if particles[0] == 1.0:  # photon gamma
                    bm = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 9.0:  # p-
                    pim = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )
                if particles[0] == 8.0:  # p+
                    pip = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

            ptarget = vectors.FourVector(.938, 0., 0., 0.)
            initp = bm + ptarget
            finalp = pip + pim + p
            pi0 = initp + finalp
            pmeson = pip + pim + pi0
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = vectors.ThreeVector(0., 1., 0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.length()
            alpha = numpy.arccos(cosAlpha)
            sys.stdout.write(str(event) + "\r")
            sys.stdout.flush()
            self.alphalist.append(alpha)

    def analyze22(self):
        """
        p p+ p-
        """
        for event in self.gampList:
            for particles in event:
                if particles[0] == 14.0:  # proton
                    pp = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )
                if particles[0] == 1.0:  # photon gamma
                    bm = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )
                if particles[0] == 9.0:  # p-
                    pim = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )
                if particles[0] == 8.0:  # p+
                    pip = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

            pmeson = pip + pim
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = vectors.ThreeVector(0.,1.,0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.length()
            alpha = numpy.arccos(cosAlpha)
            self.alphalist.append(alpha)

    def analyze24(self):
        """
            p k+ k-
        """
        for event in self.gampList:
            for particles in event:
                if particles[0] == 14.0:  # proton
                    pp = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 1.0:  # photon gamma
                    bm = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 12.0:  # K-
                    km = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 11.0:  # K+
                    kp = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

#            target = FourVector(.938, 0., 0., 0.)
            pmeson = kp + km  # K+ K-

#            if bm.z > 4.4:
#                miss = bm + target - kp - km
#                totalmiss = bm + target - kp - kp - pp
            #  determine alpha
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = vectors.ThreeVector(0., 1., 0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.length()
            alpha = numpy.arccos(cosAlpha)
            self.alphalist.append(alpha)

    def analyze42(self):
        """
        gamma p --> p Ks Ks (pi+ pi- pi+ pi-)
        """
        nks = 0
        for event in self.gampList:
            for particles in event:
                if particles[0] == 14.0:  # proton
                    p = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 1.0:  # photon gamma
                    bm = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 16.0:  # Ks
                    if nks == 0:
                        ks1 = vectors.FourVector(
                            numpy.float64(particles[1]),
                            numpy.float64(particles[2]),
                            numpy.float64(particles[3]),
                            numpy.float64(particles[4])
                        )

                    else:
                        ks2 = vectors.FourVector(
                            numpy.float64(particles[1]),
                            numpy.float64(particles[2]),
                            numpy.float64(particles[3]),
                            numpy.float64(particles[4])
                        )

                    nks += 1

            pmeson = ks1 + ks2
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = vectors.ThreeVector(0., 1., 0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.length()
            alpha = numpy.arccos(cosAlpha)

            self.alphalist.append(alpha)

    def analyzeEtaPiN(self):
        for event in self.gampList:
            for particles in event:
                if particles[0] == 13.0:  # neutron
                    n = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 1.0:  # photon gamma
                    bm = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 12.0:  # eta
                    eta = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

                if particles[0] == 11.0:  # p+
                    pip = vectors.FourVector(
                        numpy.float64(particles[1]),
                        numpy.float64(particles[2]),
                        numpy.float64(particles[3]),
                        numpy.float64(particles[4])
                    )

            pmeson = eta + pip
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = vectors.ThreeVector(0., 1., 0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.length()
            alpha = numpy.arccos(cosAlpha)

            self.alphalist.append(alpha)

    def toFile(self):
        """
            Saves the list to a file.
        """
        f = open(os.path.join(self.indir, self.alphaName), 'w')
        for alpha in self.alphalist:
            f.write(str(alpha) + "\n")
        f.close()

indir = sys.argv[2]
gfile = sys.argv[3]
mode = sys.argv[1]
a = GenerateAlphas(mode, indir, gfile)
a.toFile()

