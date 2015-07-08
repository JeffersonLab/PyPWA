import numpy,sys, os
from iminuit import Minuit

def intFn(kVars,params): # Do not change the name of this function
    """
        This is where you define your intensity function. Do not change the name of the function. 
        The names of the arguments are up to you, but they both need to be dictionaries, with the 
        first one being the kinematic variables from a list. And the second
        being the fitted parameters. All fitted parameters need to be floating point numbers. If a
        parameter of your function is a complex number make the real part one fitted variable and
        the imaginary part another. Your function should return a float. 
    """
    return (kVars['s']**2)*(kVars['t']**3)*params["A1"] #example

def parFn(A1,A2): # Do not change the name of this function
    """
        This function will be largely the same for all instances. This only needs to take the same arguments as 
        the initial value dictionary defined below and instantiate the params dictionary below and call the 
        generalFit.calcLnLike function below it with params as it's argument. This is so minutit can fit those
        parameters with your pre defined initial values. 
        
        Un-comment the return statement that you want to use. Only one can be used at a time. 
    """
    params = {'A1':A1,'A2':A2} 
    return gF.calcLnLikeExtUB(params) # Extended Un-Binned
#    return gF.calcLnLikeUExtUB(params) # Un-Extended Un-Binned
#    return gF.calcLnLikeExtB(params) # Extended Binned
#    return gF.calcLnLikeUExtB(params) # Un-Extended Binned
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
    print nTrue

from generalFitting import generalFit # Do not change this line
dataDir="./kvArgs.txt" #filepath for data text file
accDir="./kvArgsAcc.txt" #filepath for accepted Monte Carlo text file
QDir="./QFactor.txt" #filepath for Q probability factor file. Leave empty if you do not have one. 
genLen=3000000 #Integer value for number of generated Monte Carlo events
reLoad=False #Boolean value for reparsing the data and acc text files and overwriting their npy files
initial={'A1':.01,'A2':.01,'errordef':0.5}#initial values of fitted parameters as well as other iminuit arguments (do not change errordef) 
gF = generalFit(dataDir=dataDir,accDir=accDir,QDir=QDir,genLen=genLen,initial=initial,reLoad=reLoad)
"""
    In the above line do not change the names of any of the arguments but set the values to the directories
    Of your data file, accepted MC file, list of Q Factors(If you do not account
    for Q then leave it as an empty string("") and Q will be set to 1.0 for all events and be inconsequential),
    an integer value for the number of generated MC events for this fit and a boolean value for reloading 
    text files of kinimatic variables, since they do not automatically overwrite their npy files when the are changed,
    and a dictionary of all initial values for fitted parameters, as well as any other iMinuit fitting aruguments. 
    See iMinuit docs for more information. 
"""
