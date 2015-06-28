#! /apps/anaconda/bin/python2
import argparse
import numpy, sys, os
from gampParticle import gampParticle
from gampEvent import gampEvent
from gampTranslator import gampTranslator


class gampMasker (object):

    def __init__(self,File=None,pfFile=None,wnFile=None):
        
        self.File=File
        if "gamp" in self.File:
            self.gampT = gampTranslator(self.File)
            if not os.path.isfile(self.File.rstrip(".gamp")+".npy"):
                numpy.save(self.File.rstrip(".gamp")+".npy",gampT.translate(self.File.rstrip(".gamp")+".npy"))
            self.gampList=numpy.load(self.File.rstrip(".gamp")+".npy")
        elif "txt" in self.File:
            if not os.path.isfile(self.File.rstrip(".txt")+".npy"):
                self.gampList = kvParser(self.File)
                numpy.save(self.File.rstrip(".txt")+".npy",self.gampList)
            else:
                self.gampList = numpy.load(self.File.rstrip(".txt")+".npy")
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
            for n in range(self.gampList.shape[0]):
                if "gamp" in self.File:
                    pfEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.pfList[n])==1.0:
                        pfEvent.writeGamp(pfOut)
                if "txt" in self.File:
                    if float(self.pfList[n])==1.0:
                        pfEvent = self.gampList[n]
                        for i in pfEvent.keys():
                            if len(pfEvent) > 1:
                                pfOut.write(str(i)+"="+str(pfEvent.pop(i))+",")
                            elif len(pfEvent) == 1:
                                pfOut.write(str(i)+"="+str(pfEvent.pop(i))+"\n")

    def maskWN(self):
        with open(args.weighted_out,'w+') as wnOut:
            for n in range(self.gampList.shape[0]):
                if "gamp" in self.File:
                    wnEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.wnList[n])==1.0:
                        wnEvent.writeGamp(wnOut)
                if "txt" in self.File:
                    if float(self.wnList[n])==1.0:
                        wnEvent = self.gampList[n]
                        for i in wnEvent.keys():
                            if len(wnEvent) > 1:
                                wnOut.write(str(i)+"="+str(wnEvent.pop(i))+",")
                            elif len(wnEvent) == 1:
                                wnOut.write(str(i)+"="+str(wnEvent.pop(i))+"\n")

    def maskBoth(self):
        with open(args.both_out,'w+') as btOut:
            for n in range(self.gampList.shape[0]):
                if "gamp" in self.File:
                    btEvent = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        btEvent.writeGamp(btOut)
                if "txt" in self.File:
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        btEvent = self.gampList[n]
                        for i in btEvent.keys():
                            if len(btEvent) > 1:
                                btOut.write(str(i)+"="+str(btEvent.pop(i))+",")
                            elif len(btEvent) == 1:
                                btOut.write(str(i)+"="+str(btEvent.pop(i))+"\n")

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
    if len(gM.gampList) == len(gM.pfList):
        if args.accepted_out != "":
            gM.maskPF()
        else:
            print "Need a filepath to save new accepted file to."
            exit()
    else:
        print "PF mask and file not equal lengths."
        exit() 

gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.weighted_mask != "":
    if len(gM.gampList) == len(gM.wnList):
        if args.weighted_out != "":
            gM.maskWN()
        else:
            print "Need a filepath to save new weighted file to."
            exit()
    else:
        print "Weighted mask and file not equal lengths."
        exit() 

gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.both_masks:
    if len(gM.gampList) == len(gM.pfList):
        if args.accepted_out != "":
            if len(gM.gampList) == len(gM.wnList):
                if args.weighted_out != "":
                    gM.maskBoth()
                else:
                    print "Need a filepath to save new weighted file to."
                    exit()
            else:
                print "Weighted mask and file not equal lengths."
                exit() 
        else:
            print "Need a filepath to save new accepted file to."
            exit()
    else:
        print "PF mask and file not equal lengths."
        exit() 

gM = gampMasker(File=args.file,pfFile=args.acceptance_mask,wnFile=args.weighted_mask)

if args.custom_mask:
    gM.maskAny()

