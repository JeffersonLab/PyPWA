"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy
from PyPWAiSOBAR.model.complexV import complexV

def nTrue(resonances,waves,mass,normint):
    """
    Returns the number of events for all resonances and waves for the specified mass and normalization integral.
    """
    ret=0.
    for resonance1 in resonances:
        #print"resonance1=",resonance1.r0
        for resonance2 in resonances:
            #print"resonance2=",resonance2.r0
            for wave1 in waves:
                for wave2 in waves:
                    v1=complexV(resonance1,wave1,waves,normint,mass)
                    v2=numpy.conjugate(complexV(resonance2,wave2,waves,normint,mass))
                    psi=normint[wave1.epsilon,wave2.epsilon,waves.index(wave1),waves.index(wave2)]
                    term=v1*v2*psi
                    ret+=term
    return ret.real

def nTrueForWave(resonances,waves,wave,mass,normint):
    """
    Returns the number of events for all resonances, for a specified wave out of the set of all waves, for the specified mass,
    and for the nomalization integral.
    """
    ret=0.
    for resonance1 in resonances:
        for resonance2 in resonances:
            v1=complexV(resonance1,wave,waves,normint,mass)
            v2=numpy.conjugate(complexV(resonance2,wave,waves,normint,mass))
            psi=normint[wave.epsilon,wave.epsilon,waves.index(wave),waves.index(wave)]
            term=v1*v2*psi
            ret+=term
    return ret.real
    
    
def nTrueForFixedV1V2(vList,waves,normint):
    """
    calculates the number of events for fitted v1 and v2 values.
    """
    ret=0.
    for wave1 in waves:
        for wave2 in waves:
            psi=normint[wave1.epsilon,wave2.epsilon,waves.index(wave1),waves.index(wave2)]
            print"psi:", psi
            ret+=vList[waves.index(wave1)]*numpy.conjugate(vList[waves.index(wave2)])*psi
    return ret.real
    
def nTrueForFixedV1V2AndWave(v,waves,wave,normint):
    """
    calculates the number of events for fitted v1 and v2 values for a specific
    wave.
    """
    return v*numpy.conjugate(v)*normint[wave.epsilon,wave.epsilon,waves.index(wave),waves.index(wave)]

def partialDerivativeNTrue(rawNormalizationIntegral,vList,waves,wave,realFlag):
    """
    Returns the value of the partial derivative of nTrue
    """
    ret=0.
    for wv in waves:
        if realFlag==True:
            ret+=rawNormalizationIntegral[wave.epsilon,wv.epsilon,waves.index(wave),waves.index(wv)]*numpy.real(vList[waves.index(wv)])
        if realFlag==False:
            ret+=rawNormalizationIntegral[wave.epsilon,wv.epsilon,waves.index(wave),waves.index(wv)]*numpy.imag(vList[waves.index(wv)])
    return 2.*ret

def constructJacobianVector(rawNormalizationIntegral,vList,waves):
    """
    Returns a list representing the jacobian vector for specifed set of waves.
    """
    jacobianVector=[]
    for wave in waves:
        realFlag=True
        rPartial=partialDerivativeNTrue(rawNormalizationIntegral,vList,waves,wave,realFlag)
        realFlag=False
        iPartial=partialDerivativeNTrue(rawNormalizationIntegral,vList,waves,wave,realFlag)
        jacobianVector.append(rPartial)
        jacobianVector.append(iPartial)
    return numpy.asmatrix(jacobianVector)

def calcStatSquaredError(covarianceMatrix,rawNormalizationIntegral,vList,waves):
    """
    Calculates the square of the statistical error for nTrue
    """
    jacobian=constructJacobianVector(rawNormalizationIntegral,vList,waves)
    return jacobian*covarianceMatrix*numpy.transpose(jacobian)

    
def calcSysSquaredError(iSets):
    """
    Calculates the square of the systematic error for nTrue
    """
    N=float(len(iSets))
    iHat=numpy.complex(0.,0.)
    
    for iSet in iSets:
        iHat+=sum(iSet)
    
    iHat=iHat/N
    
    ret=numpy.complex(0.,0.)
    for iSet in iSets:
        for i in iSet:
            ret+=(iHat-i)*(iHat-i)
    return ret/N

def calcNTrueError(iSets,covarianceMatrix,rawNormalizationIntegral,vList,waves):
    """
    Calculates the total error in nTrue including the systematic and statistical error
    """
    return calcSysSquaredError(iSets)+calcStatSquaredError(covarianceMatrix,rawNormalizationIntegral,vList,waves)
