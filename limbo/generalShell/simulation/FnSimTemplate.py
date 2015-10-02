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
 
def simFn():
    """
        This is the function that will do the actual simulating. Fill out the filepaths below.
    """
    
    nTrueDir=""#Location to save the nTrue File
    inputKVDir=""#Loaction of the Generated MC KV text File
    outputWeightDir=""#Location where the weighted mask file will be saved
                    
    iList = numpy.load("")#Location of the list of intensities. 

    iMax = numpy.load("")#Location of the Maximum intensity of the WHOLE mass range
                
    gS.simulate(nTrueDir,inputKVDir,outputWeightDir,iList,iMax)


from generalSim import generalSim
inputKVDir=""#Loaction of the Generated MC KV File(Same as above)
gS = generalSim(KVDir = inputKVDir)
if sys.argv[1] == "i":
    numpy.save("",gS.calcIList({'A1':7.,'A2':-3.0,'A3':0.37,'A4':0.037,'A5':0.121}))#example The first argument of numpy.save() is the filepath of the iList to be saved.
elif sys.argv[1] == "s":
    simFn()
