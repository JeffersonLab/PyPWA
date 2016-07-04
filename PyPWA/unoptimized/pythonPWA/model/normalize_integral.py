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

import numpy

from PyPWA.unoptimized.pythonPWA.model.spinDensity import spinDensity
from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


class NormalizeIntegral(object):

    def __init__(self, waves=[], alpha_list=[], beam_polarization=0.0):
        """
        Represents a normalization integral. To compute the value of the
        normalization integral call NormalizeIntegral.execute(). To save
        the normalization integral to a directory call
        NormalizeIntegral.save()
        """
        self.waves = waves
        self.alphaList = alpha_list
        self.beamPolarization = float(beam_polarization)

        self.ret = numpy.ndarray((2, 2, len(waves), len(waves)), 'c16')
        self.ret[:, :, :, :] = numpy.complex(0., 0.)

    def execute(self):
        """
        Returns the normalization integral for the waves, alphas, and
        beam polarization.

        Note that the normalization integral is stored as a numpy ndarray
        with 4 dimensions.

        The indexing of the normalization integral is
        [wave1.epsilon,
        wave2.epsilon,
        waves.index(wave1),
        waves.index(wave2)].

        This means that the first 2 dimensions
        (wave1.epsilon,wave2.epsilon) have length of 2. The last 2
        dimensions (waves.index(wave1),waves.index(waves2)) have length
        equal to the number of waves to be represented in this
        normalization integral.
        """
        for event_number, alpha in enumerate(self.alphaList):
            spindensity = spinDensity(self.beamPolarization, alpha)
            for wave1 in self.waves:
                for wave2 in self.waves:
                    temp=wave1.complexamplitudes[event_number]*numpy.conj(wave2.complexamplitudes[event_number])*spindensity[wave1.epsilon,wave2.epsilon]
                    self.ret[wave1.epsilon,wave2.epsilon,self.waves.index(wave1),self.waves.index(wave2)]+=temp

        buffe=self.ret*(1./float(event_number))
        self.ret=buffe
        return self.ret

    def save(self,directory):
        """
        Saves the current value of the normalization integral.  Note that if this is called before
        NormalizeIntegral.execute() it will save an ndarray of complex 0's to the specified file.
        """
        numpy.save(os.path.join(directory,"normint.npy"),self.ret)

    def writeToAscii(self,directory):
        """
        This function writes the values of the normalization integral to a text file.
        Make sure to run execute method first.
        """
        outfile=open(os.path.join(directory,"normint.txt"),'w')
        outfile.write(str(len(self.waves))+"\n")
        outfile.write(str(len(self.alphaList))+"\n")
        for eps1 in range(2):
            for eps2 in range(2):
                outfile.write(str(len(self.waves))+" "+str(len(self.waves))+" "+str(eps1)+" "+str(eps2)+"\n")
                for index1 in range(len(self.waves)):
                    for index2 in range(len(self.waves)-1):
                        tempcomplex=self.ret[eps1,eps2,index1,index2]
                        tempreal=numpy.real(tempcomplex)
                        tempim=numpy.imag(tempcomplex)
                        outfile.write(" ("+str(tempreal)+" + i "+str(tempim)+") , ")
                    tempcomplex=self.ret[eps1,eps2,index1,int(len(self.waves)-1)]
                    tempreal=numpy.real(tempcomplex)
                    tempim=numpy.imag(tempcomplex)
                    outfile.write(" ("+str(tempreal)+" + i "+str(tempim)+")")
                    outfile.write("\n")
                outfile.write("\n")
                outfile.write(str(len(self.waves))+"\n")
                for wave in self.waves:
                    outfile.write(wave.filename+" "+str(self.waves.index(wave))+"\n")
        outfile.close()

