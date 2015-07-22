#! /apps/anaconda/bin/python2
import argparse
import numpy, sys, os
from gampParticle import gampParticle
from gampEvent import gampEvent

class gampMasker (object):

    def __init__(self,File=None,pfFile=None,wnFile=None):
        
        self.File=File
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
                i = 0
                n = 0  
                x = -1
                event=np.zeros(shape=[1,6])
                for line in fileinput.input([self.File]):
                    if i == 0:
                        x = int(line)              
                        event.resize(x+1,6)         
                        event[0,0] = float(line)           
                        i+=1
                    elif i < x and i!= 0:                     
                        particle = line.split() 
                        event[i,0]= particle[0]
                        event[i,1]= particle[1]
                        event[i,2]= particle[2]
                        event[i,3]= particle[3]
                        event[i,4]= particle[4]
                        event[i,5]= particle[5].strip("\n")
                        i+=1
                    elif i == x:
                        particle = line.split()
                        event[i,0]= particle[0]
                        event[i,1]= particle[1]
                        event[i,2]= particle[2]
                        event[i,3]= particle[3]
                        event[i,4]= particle[4]
                        event[i,5]= particle[5].strip("\n")
                        if float(self.pfList[n])==1.0:
                            Event = self.writeEvent(event)
                            Event.writeGamp(pfOut)
                        i = 0  
                        x = -1
                        n+=1
            if "txt" in self.File:
                n = 0 
                for line in fileinput.input([self.File]):        
                    if float(self.pfList[n])==1.0:
                        pfOut.write(line)
                    n+=1

    def maskWN(self):
        with open(args.weighted_out,'w+') as wnOut:
            if "gamp" in self.File:
                i = 0
                n = 0  
                x = -1
                event=np.zeros(shape=[1,6])
                for line in fileinput.input([self.File]):
                    if i == 0:
                        x = int(line)              
                        event.resize(x+1,6)         
                        event[0,0] = float(line)           
                        i+=1
                    elif i < x and i!= 0:                     
                        particle = line.split() 
                        event[i,0]= particle[0]
                        event[i,1]= particle[1]
                        event[i,2]= particle[2]
                        event[i,3]= particle[3]
                        event[i,4]= particle[4]
                        event[i,5]= particle[5].strip("\n")
                        i+=1
                    elif i == x:
                        particle = line.split()
                        event[i,0]= particle[0]
                        event[i,1]= particle[1]
                        event[i,2]= particle[2]
                        event[i,3]= particle[3]
                        event[i,4]= particle[4]
                        event[i,5]= particle[5].strip("\n")
                        if float(self.wnList[n])==1.0:
                            Event = self.writeEvent(event)
                            Event.writeGamp(wnOut)
                        i = 0  
                        x = -1
                        n+=1
            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.wnList[n])==1.0:
                        wnOut.write(line)
                    n+=1

    def maskBoth(self):
        with open(args.both_out,'w+') as btOut:
            if "gamp" in self.File:
                i = 0
                n = 0  
                x = -1
                event=np.zeros(shape=[1,6])
                for line in fileinput.input([self.File]):
                    if i == 0:
                        x = int(line)              
                        event.resize(x+1,6)         
                        event[0,0] = float(line)           
                        i+=1
                    elif i < x and i!= 0:                     
                        particle = line.split() 
                        event[i,0]= particle[0]
                        event[i,1]= particle[1]
                        event[i,2]= particle[2]
                        event[i,3]= particle[3]
                        event[i,4]= particle[4]
                        event[i,5]= particle[5].strip("\n")
                        i+=1
                    elif i == x:
                        particle = line.split()
                        event[i,0]= particle[0]
                        event[i,1]= particle[1]
                        event[i,2]= particle[2]
                        event[i,3]= particle[3]
                        event[i,4]= particle[4]
                        event[i,5]= particle[5].strip("\n")
                        if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                            Event = self.writeEvent(event)
                            Event.writeGamp(wnOut)
                        i = 0  
                        x = -1
                        n+=1
            if "txt" in self.File:
                n = 0 
                for line in fileinput.input([self.File]):
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        btOut.write(line)
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

