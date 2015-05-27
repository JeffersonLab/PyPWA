import numpy,sys, os
from iminuit import Minuit

def intFn(kVars,params): # Do not change the name of this function
    """
        This is where you define your intensity function. Do not change the name of the function. 
        The names of the arguments are up to you, but they both need to be dictionaries, with the 
        first one being the kinematic variables from a list. And the second
        being the fitted parameters. All fitted parameters need to be floating point numbers. If a
        parameter of your function is a complex number make the real part one fitted variable and
        the imaginary part another. Your function should return a numpy.complex(real,imaginary) 
        as below. 
    """
    return numpy.complex((kVars['s']**2)*(kVars['t']**3)*params["A1"],params['A2']*kVars['u']) #example

def parFn(A1,A2): # Do not change the name of this function
    """
        This function will be largely the same for all instances. This only needs to take the same arguments as 
        the initial value dictionary defined below and instantiate the params dictionary below and call the 
        generalFit.calcLnLike function below it with params as it's argument. This is so minutit can fit those
        parameters with your pre defined initial values. 
    """
    params = {'A1':A1,'A2':A2} 
    return gF.calcLnLike(params) # Do not change anything on this line

def migFn(): # Do not change this line
    kwdarg = gF.initial # or this one
    m = Minuit(parFn,**kwdarg) # or this one
    m.set_strategy(0) # set strategy as an int. 0: Fast 1: More accurate 2: Slowest/most accurate
    m.set_up(0.5) # Leave this line alone
    m.migrad(ncall=1000) # set ncall >=1000

    Vvalues = m.values # Do not change
    numpy.save(os.path.join(".","Vvalues.npy"),Vvalues) # The first argument of numpy.save is the file path/name you  
                                                        # want to save the fitted values to
def nTrueFn():
    from calcNTrue import calcNTrue
    genDir = "./kvArgsGen.txt"  #<------- This should be the only thing you have to set for the  
    params = numpy.load("Vvalues.npy")     #calculation of nTrue, just set it to the generated MC file.
    nT = calcNTrue(genDir)
    nTrue = nT.calcNTrue(params)

from generalShell import generalFit # Do not change this line
dataDir="./kvArgs.txt"
accDir="./kvArgsAcc.txt"
QDir="./QFactor.txt"
initial={'A1':.01,'A2':.01,'errordef':0.5}#do not change errordef 
gF = generalFit(dataDir=dataDir,accDir=accDir,QDir=QDir,initial=initial)
"""
    In the above line do not change the names of any of the arguments but set the values to the directories
    Of your data file, accepted MC file, list of Q Factors(If you do not account
    for Q then leave it as an empty string("") and Q will be set to 1.0 for all events and be inconsequential),
    and a dictionary of all initial values for fitted parameters, as well as any other iMinuit fitting aruguments. 
    See iMinuit docs for more information. 
"""
