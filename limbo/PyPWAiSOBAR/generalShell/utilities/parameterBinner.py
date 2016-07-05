#! /apps/anaconda/bin/python2
import argparse
from matplotlib import pyplot as plt
import numpy, sys, os
import fileinput

class parameterBinner (object):

    def __init__(self,param=None,inputName=None,outputName=None,binN=None):
        self.param = param
        self.inputName = inputName
        self.outputName = outputName
        self.binN = binN
        self.params = numpy.empty(shape=(1))

    def binner(self):
        n = 0
        passed = 0
        dots = 1
        spaces = 9
        for line in fileinput.input([self.inputName]):
            self.params.resize(1+n)
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            if not self.param in kvAx:
                exit("KeyError: '"+self.param+"' Parameter not in input file.")
            self.params[n] = kvAx[self.param]
            if passed == 100000:
                sys.stdout.write("Reading"+"."*dots+" "*spaces+"\r")
                sys.stdout.flush()
                passed = 0
                dots+=1
                spaces-=1
            if spaces == 0:
                dots = 0
                spaces = 10
            n+=1
            passed+=1
        print("Read "+str(n)+" lines from "+self.inputName)
        hist = plt.hist(self.params,int(self.binN),histtype="step")        
        bins = hist[0]
        pars = hist[1]
        self.writer(bins,pars)
        
    def writer(self,bins,pars):
        with open(self.outputName,"w+") as out:
            n = 0
            for i in range(len(bins)):
                out.write(self.param+"="+str(pars[i])+",BinN="+str(bins[i])+"\n")
                n+=1    
        print("Wrote "+str(n)+" lines to "+self.outputName)
     
parser = argparse.ArgumentParser(description="""A tool for binning a single parameter of a PyPWA text format file into a defined number of bins.
Writes a text file in PyPWA format that can be directly used by the PyPWA generalFitter binned likelihood fitter.""")
parser.add_argument("-n","--number_of_bins",help="The number of bins. Defaults to 300.",action="store",default=300)
parser.add_argument("-hist","--show_histogram",help="Show a histogram of the new bins.",action="store_true")
parser.add_argument("parameter",help="The parameter to be binned in.")
parser.add_argument("inputFile",help="The full filepath/name of the text file to be binned.")
parser.add_argument("outputFile",help="The full filepath/name of the text file to be written.")
args = parser.parse_args()
if not os.path.isfile(args.inputFile):
    exit('IOError: No such file or directory: '+"'"+args.inputFile+"'")
pB = parameterBinner(param=args.parameter,inputName=args.inputFile,outputName=args.outputFile,binN=args.number_of_bins)
pB.binner()
if args.show_histogram:
    print("Plotting")
    plt.show()
