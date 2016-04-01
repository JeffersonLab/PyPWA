
import numpy

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ExtendedLikelihoodAmplitude(object):
    def __init__(self, generated_length):
        self._processed = 1.0/generated_length

    def likelihood(self, data, accepted, qfactor):
        """Calculates the extended likelihood function
        Args:
            data:
            accepted:
            qfactor:
        """
        masked_data = numpy.ma.masked_equal(data, 0)
        masked_accepted = numpy.ma.masked_equal(accepted, 0)
        return -(numpy.sum(qfactor * numpy.ma.log(masked_data))) + (self._processed * numpy.ma.sum(masked_accepted))


class UnextendedLikelihoodAmplitude(object):
    def likelihood(self, data, binned, qfactor):
        """Calculates the binned likelihood function
        Args:
            data:
            binned:
            qfactor:
        """
        masked_data = numpy.ma.masked_equal(data, 0)
        return -(numpy.ma.sum(qfactor * binned * numpy.ma.log(masked_data)))


class Chi(object):
    def likelihood(self, data, binned, qfactor):
        """Calculates the ChiSquare function
        Args:
            data:
            binned:
            qfactor:
        """
        masked_data = numpy.ma.masked_equal(data, 0)
        return ((masked_data - binned)**2) / binned
