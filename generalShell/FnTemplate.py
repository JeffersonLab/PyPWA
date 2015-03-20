import numpy,sys, os
from FourVec import FourVector
from iminuit import Minuit

def ampFn(kVars,params): # Do not change the name of this function
    """
        This is where you define your intensity function. Do not change the name of the function. 
        The names of the arguments are up to you, but they both need to be dictionaries, with the 
        first one being the kinematic variables, either from a gamp event or a list. And the second
        being the fitted parameters. All fitted parameters need to be floating point numbers. If a
        parameter of your function is a complex number make the real part one fitted variable and
        the imaginary part another. Your function should return a numpy.complex(real,imaginary) 
        as below. 
    """
    return numpy.complex((kVars['s']**2)*(kVars['t']**3)*params["A1"],params['A2']*kVars['u']) #example

def kvFn(event): # Do not change anything on this line
    """
        This is where you define your function that returns a dictionary of the kinematic variables
        calculated from a PyPWA.gampEvent object. This is an example of the calculation of the
        Mandelstram variables(S,T,U) from gamma + P -> Pi+ Pi- Pi0 data, but it can be anything
        that takes a gampEvent object and returns a dictionary that matches the above defined function.
        If you are using a straight list of variables, then this function will never be called. After
        the definition line just put "pass" indented once, with no return statement. 
    """

    for particles in event.particles:
        if particles.particleID == 14.0: #recoil proton
            p = FourVector(float(particles.particleE), 
                            float(particles.particleXMomentum),
                            float(particles.particleYMomentum),
                            float(particles.particleZMomentum))
        if particles.particleID == 1.0: #photon gamma
            bm = FourVector(float(particles.particleE), 
                            float(particles.particleXMomentum),
                            float(particles.particleYMomentum),
                            float(particles.particleZMomentum))
        if particles.particleID == 9.0: #p-
            pim = FourVector(float(particles.particleE), 
                            float(particles.particleXMomentum),
                            float(particles.particleYMomentum),
                            float(particles.particleZMomentum))
        if particles.particleID == 8.0: #p+
            pip = FourVector(float(particles.particleE), 
                            float(particles.particleXMomentum),
                            float(particles.particleYMomentum),
                            float(particles.particleZMomentum))
    ptarget = FourVector(.938, 0.,0.,0.)
    initp = bm + ptarget
    finalp = pip + pim + p
    pi0 = initp - finalp
    P1 = FourVector(bm.E,0.0,0.0,bm.E)
    P2 = ptarget
    P3 = pip + pim + pi0
    P4 = p   

    s= (P1+P2).dot(P1+P2)
    t= (P1-P3).dot(P1-P3)
    u= (P1-P4).dot(P1-P4)
    return {'s':s,'t':t,'u':u} #example

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
    m.migrad(ncall=1000) # set ncall >1000

    Vvalues = m.values # Do not change
    numpy.save(os.path.join(".","Vvalues.npy"),Vvalues) # The first argument of numpy.save is the file path/name you  
                                                        # want to save the fitted values to

from generalShell import generalFit # Do not change this line
gF = generalFit(dataDir="./kvArgs.txt",genDir="./kvArgsGen.txt",QDir="./QFactor.txt",initial={'A1':.01,'A2':.01})
"""
    In the above line do not change the names of any of the arguments but set the values to the directories
    Of your data file(either gamp or parameter list), generated MC file, list of Q Factors(If you do not account
    for Q then leave it as an empty string("") and Q will be set to 1.0 for all events and be inconsequential),
    and a dictionary of all initial values for fitted parameters. 
"""
