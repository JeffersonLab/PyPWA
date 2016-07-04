import numpy


# TODO: Fix the memory issues with this file.
# TODO: Extract the file logic from this file.
# TODO: Move all these functions into a single object.

def gamp_length(path):
    ins = open(path)
    for line in ins:
        length = line.strip("\n")
    return float(length)


def count_alphas(path):
        """
        Returns the length of an alpha angle file.

        Args:
        path (string):

        Returns:
        Int equivalent to the length of the alpha file.
        """

        Alpha = open(path, 'length')
        AlphaList = Alpha.readlines()
        return float(len(AlphaList))


def etaX(apath, rpath):
    """
    Calculates the acceptance.

    Returns:
    Float value of the acceptance.
    """
    etaX = (count_alphas(apath) / count_alphas(rpath))
    return etaX


def nExpForFixedV1V2(vList, waves, normint, apath, rpath):
    """
    calculates the number of _events for fitted v1 and v2 values.
    """
    ret=0.
    for wave1 in waves:
        for wave2 in waves:
            psi = normint[
                wave1.epsilon,
                wave2.epsilon,
                waves.index(wave1),
                waves.index(wave2)
            ]

            ret += vList[waves.index(wave1)] \
                   * numpy.conjugate(vList[waves.index(wave2)]) \
                   * psi

    return etaX(apath, rpath) * ret.real


def nExpForFixedV1V2AndWave(v, waves, wave, normint, apath, rpath):
    """
    calculates the number of _events for fitted v1 and v2 values for a
    specific wave.
    """
    extracted_integral = normint[
        wave.epsilon,
        wave.epsilon,
        waves.index(wave),
        waves.index(wave)
    ]

    acceptance = etaX(apath, rpath)

    final_value = acceptance * v * numpy.conjugate(v) * extracted_integral

    return final_value
