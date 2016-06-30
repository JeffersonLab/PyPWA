import numpy


def gampLen(path):
    ins = open(path)
    for line in ins:
        leng = line.strip("\n")
    return float(leng)

def countAlphas(path):
        """
        Returns the length of an alpha angle file.

        Args:
        path (string):

        Returns:
        Int equivalent to the length of the alpha file.
        """
        Alpha = open(path,'r')
        AlphaList = Alpha.readlines()
        
        return float(len(AlphaList))  
        
def etaX(apath,rpath):
    """
    Calculates the acceptance.

    Returns:
    Float value of the acceptance.
    """
    #etax=(gampLen(apath)/gampLen(rpath))
    etaX=(countAlphas(apath)/countAlphas(rpath))
    return etaX 

def nExpForFixedV1V2(vList,waves,normint,apath,rpath):
    """
    calculates the number of _events for fitted v1 and v2 values.
    """
    ret=0.
    for wave1 in waves:
        for wave2 in waves:
            psi=normint[wave1.epsilon,wave2.epsilon,waves.index(wave1),waves.index(wave2)]
            
            ret+=vList[waves.index(wave1)]*numpy.conjugate(vList[waves.index(wave2)])*psi
    return etaX(apath,rpath)*ret.real
    
def nExpForFixedV1V2AndWave(v,waves,wave,normint,apath,rpath):
    """
    calculates the number of _events for fitted v1 and v2 values for a specific
    wave.
    """
    return etaX(apath,rpath)*v*numpy.conjugate(v)*normint[wave.epsilon,wave.epsilon,waves.index(wave),waves.index(wave)]
