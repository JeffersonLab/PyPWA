#! /u/apps/anaconda/bin/python2.7
import numpy,sys, os
import math



def intFn(kVars,params): # Do not change the name of this function
    """
        This is where you define your intensity function. Do not change the name of the function. 
        The names of the arguments are up to you, but they both need to be dictionaries, with the 
        first one being the kinematic variables, either from a gamp event or a list. And the second
        being the fitted parameters. All fitted parameters need to be floating point numbers. If a
        parameter of your function is a complex number make the real part one fitted variable and
        the imaginary part another. Your function should return a float. 
    """
    return (kVars['s']**2)*(kVars['t']**3)*params["A1"] #example

def kvFn(event): # Do not change anything on this line    
    """
        This is where you define the function that accepts a pythonPWA gamp event object and returns
        a keyed dictionary of the kinematic variables of the event for your intensity. This is an example 
        of best practices for calculating the Mandulstrum variables from a gamma P -> Pi+ Pi- Pi0 event. 
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
 
def simFn():
    """
        This is the function that will do the actual simulating. Fill out the filepaths below.
    """
    
    nTrueDir=""#Location to save the nTrue File
    inputGampDir=""#Loaction of the Generated MC Gamp File
    inputPfDir=""#Location of the Generated acceptance PF file
    outputPFGampDir=""#Location where the accepted, unweighted Gamp file will be saved
    outputRawGampDir=""#Location where the unaccepted, weighted Gamp file will be saved
    outputAccGampDir=""#Location where the accepted, weighted Gamp file will be saved
                    
    iList = numpy.load("")#Location of the list of intensities. 

    iMax = numpy.load("")#Location of the Maximum intensity of the WHOLE fit
                
    gS.simulate(nTrueDir,inputGampDir,outputRawGampDir,outputAccGampDir,inputPfDir,outputPFGampDir,iList,iMax)


from generalSim import generalSim
inputGampDir=""#Loaction of the Generated MC Gamp File(Same as above)
reLoad = False#Boolean value for reparsing the generated MC gamp file and overwriting its npy files
gS = generalSim(gampDir = inputGampDir,reLoad=reLoad)
if sys.argv[1] == "i":
    numpy.save("",gS.calcIList({'A1':7.,'A2':-3.0,'A3':0.37,'A4':0.037,'A5':0.121}))#example The first argument of numpy.save() is the filepath of the iList to be saved.
elif sys.argv[1] == "s":
    simFn()
