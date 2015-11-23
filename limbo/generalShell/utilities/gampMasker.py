#! /apps/anaconda/bin/python2
import argparse
import numpy, sys, os
import fileinput
sys.path.append("../pythonPWA/pythonPWA")
from dataTypes.gampParticle import gampParticle
from dataTypes.gampEvent import gampEvent
from fileHandlers.gampTranslator import gampTranslator


class gampMasker (object):

    def __init__(self,File=None,pfFile=None,wnFile=None):

        self.File=File
        if "gamp" in self.File:
            self.gampT = gampTranslator(self.File)
            if not os.path.isfile(self.File.rstrip(".gamp")+".npy"):
                numpy.save(self.File.rstrip(".gamp")+".npy",self.gampT.translate(self.File.rstrip(".gamp")+".npy"))
      #      self.gampList=numpy.load(self.File.rstrip(".gamp")+".npy")
            self.gampList=numpy.load(self.File.rstrip(".gamp")+".npy")
        elif "txt" in self.File:
            #if not os.path.isfile(self.File.rstrip(".txt")+".npy"):
            #    self.gampList = kvParser(self.File)
            #    numpy.save(self.File.rstrip(".txt")+".npy",self.gampList)
            #else:
            pass

        self.pfFile=pfFile
        if os.path.isfile(self.pfFile):
            self.pfList=numpy.loadtxt(self.pfFile)
        else:
            self.pfList=[0]

        self.wnFile=wnFile
        if os.path.isfile(self.wnFile):
            self.wnList=numpy.load(self.wnFile)
        else:
            self.wnList=[0]

    def maskPF(self):
        with open(args.accepted_out,'w+')as pfOut:
            if "gamp" in self.File:
            	n = 0
            	print self.gampList.shape[0]
                for n in range(self.gampList.shape[0]):
  #              for n in range(len(self.gampList)):
                    pfEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.pfList[n])==1.0:
                        pfEvent.writeGamp(pfOut)
                        #print "I'm writing a gampEvent (pf)!"

            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.pfList[n])==1.0:
                        pfOut.write(line)
                        #print "I'm writing a txtEvent (pf)!"
                    n+=1

    def maskWN(self):
        with open(args.weighted_out,'w+') as wnOut:
            if "gamp" in self.File:
                for n in range(self.gampList.shape[0]):
                    wnEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.wnList[n])==1.0:
                        wnEvent.writeGamp(wnOut)
                        #print "I'm writing a gampEvent (wn)!"
            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.wnList[n])==1.0:
                        wnOut.write(line)
                        #print "I'm writing a txtEvent (wn)!"
                    n+=1

    def maskBoth(self):
        with open(args.both_out,'w+') as btOut:
            if "gamp" in self.File:
                for n in range(self.gampList.shape[0]):
                    btEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        btEvent.writeGamp(btOut)
                        #print "I'm writing a gampEvent (bt)!"
            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        btOut.write(line)
                        #print "I'm writing a txtEvent (bt)!"
                    n+=1

    def maskAny(self):
        maskList = numpy.loadtxt(raw_input("Where is the custom mask text file? "))
        with open(raw_input("Where should the new file be saved? "),'w+') as mkOut:
            for n in range(self.gampList.shape[0]):
                if "gamp" in self.File:
                    mkEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(maskList[n]) == 1.0:
                        mkEvent.writeGamp(mkOut)
                if "txt" in self.File:
                    if float(self.mkList[n])==1.0:
                        mkEvent = self.gampList[n]
                        for i in mkEvent.keys():
                            if len(mkEvent) > 1:
                                mkOut.write(str(i)+"="+str(mkEvent.pop(i))+",")
                            elif len(mkEvent) == 1:
                                mkOut.write(str(i)+"="+str(mkEvent.pop(i))+"\n")


parser = argparse.ArgumentParser(description="""A tool for producing gamp files from phase space using pre-calculated mask files.""")
parser.add_argument("file",help="The full filepath/name of the gamp or text file to be masked.",default="")
parser.add_argument("-pf","--acceptance_mask",help="The full filepath/name of the pf acceptance (.txt) file to use.",default="")
parser.add_argument("-pfOut","--accepted_out",help="The full filepath/name of the accepted output file.",default="./pf_Out")
parser.add_argument("-w","--weighted_mask",help="The full filepath/name of the weight mask (.npy) file to use.",default="")
parser.add_argument("-wOut","--weighted_out",help="The full filepath/name of the weighted output file.",default="./weight_Out")
parser.add_argument("-b","--both_masks",help="Use both the acceptance and weighted masks.",action="store_true")
parser.add_argument("-bOut","--both_out",help="The full filepath/name of the accepted and weighted output file.",default="./acc_weight_Out")
parser.add_argument("-c","--custom_mask",help="Use a custom mask.",action="store_true")
args = parser.parse_args()

gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.acceptance_mask != "":
    if args.accepted_out != "":
        print "masking pf!"
        gM.maskPF()
    else:
        print "Need a filepath to save new accepted file to."
        exit()


gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.weighted_mask != "":
    if args.weighted_out != "":
    	print "masking wn!"
        gM.maskWN()
    else:
        print "Need a filepath to save new weighted file to."
        exit()

gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.both_masks:
    if args.accepted_out != "":
        if args.weighted_out != "":
            print "masking both!"
            gM.maskBoth()
        else:
            print "Need a filepath to save new weighted file to."
            exit()

    else:
        print "Need a filepath to save new accepted file to."
        exit()


gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.custom_mask:
    print "masking any!"
    gM.maskAny()

