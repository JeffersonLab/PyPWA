import numpy


class ExtendedLikelihoodAmplitude(object):
    def likelihood(self, parameters):
        """Calculates the likelihood function
        Args:
            parameters (dict): dictionary of the arguments to be sent to the function
        """
        processed_data = self._amplitude_function(self._data["data"], parameters)
        processed_accepted = self._amplitude_function(self._accepted["data"], parameters)
        return -(numpy.sum(self._data["QFactor"] * self._data["BinN"] * numpy.log(processed_data))) + \
                (self._processed * numpy.sum(self._accepted["BinN"] * processed_accepted))


class UnextendedLikelihoodAmplitude(object):
    def likelihood(self, parameters):
        """Calculates the likelihood function
        Args:
            parameters (dict): dictionary of the arguments to be sent to the function
        """
        processed_data = self._amplitude_function(self._data["data"], parameters)
        value = numpy.float64(0.0)

        for index in range(len(processed_data)):
            if self._data["BinN"][index] == 0:
                pass
            else:
                value += (numpy.sum(self._data["QFactor"][index] * self._data["BinN"][index] *
                                    numpy.log(processed_data[index])))

        return -value


class Chi(object):
    def likelihood(self, parameters):
        processed_data = self._amplitude_function(self._data["data"], parameters)
        chi = numpy.float64(0.0)
        for index in range(len(processed_data)):
            if self._data["BinN"][index] == 0:
                pass
            else:
                chi += ((processed_data[index] - self._data["BinN"][index])**2) / self._data["BinN"][index]
        return chi