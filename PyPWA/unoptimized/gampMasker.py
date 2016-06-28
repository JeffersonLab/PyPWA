import argparse
import builtins
import os
import sys
import fileinput

import numpy

from PyPWA.unoptimized.pythonPWA.fileHandlers.gampTranslator import \
    gampTranslator

from PyPWA import VERSION, STATUS, LICENSE

__author__ = ["Joshua Pond"]
__credits__ = ["Joshua Pond", "Mark Jones"]
__license__ = LICENSE
__maintainer__ = ["Mark Jones"]
__status__ = STATUS
__version__ = VERSION
__email__ = "maj@jlab.org"


class GampMasker (object):

    def __init__(self, file=None, pf_file=None, wn_file=None):

        self.File=file
        if "gamp" in self.File:
            self.gampT = gampTranslator(self.File)
            if not os.path.isfile(self.File.rstrip(".gamp")+".npy"):
                numpy.save(self.File.rstrip(".gamp")+".npy",self.gampT.translate(self.File.rstrip(".gamp")+".npy"))
            self.gampList=numpy.load(self.File.rstrip(".gamp")+".npy")
        elif "txt" in self.File:
            pass

        self.pfFile=pf_file
        if os.path.isfile(self.pfFile):
            self.pfList=numpy.loadtxt(self.pfFile)
        else:
            self.pfList=[0]

        self.wnFile=wn_file
        if os.path.isfile(self.wnFile):
            self.wnList=numpy.load(self.wnFile)
        else:
            self.wnList=[0]

    def maskPF(self):
        with open(args.accepted_out,'w+')as pfOut:
            if "gamp" in self.File:
                n = 0
                print(self.gampList.shape[0])
                for n in range(self.gampList.shape[0]):
                    pf_event = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.pfList[n])==1.0:
                        pf_event.writeGamp(pfOut)

            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.pfList[n])==1.0:
                        pfOut.write(line)
                    n += 1

    def maskWN(self):
        with open(args.weighted_out,'w+') as wnOut:
            if "gamp" in self.File:
                for n in range(self.gampList.shape[0]):
                    wn_event = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.wnList[n])==1.0:
                        wn_event.writeGamp(wnOut)
            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.wnList[n])==1.0:
                        wnOut.write(line)
                    n += 1

    def maskBoth(self):
        with open(args.both_out,'w+') as btOut:
            if "gamp" in self.File:
                for n in range(self.gampList.shape[0]):
                    bt_event = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        bt_event.writeGamp(btOut)
            if "txt" in self.File:
                n = 0
                for line in fileinput.input([self.File]):
                    if float(self.wnList[n]) == 1.0 and float(self.pfList[n])==1.0:
                        btOut.write(line)
                    n += 1

    def maskAny(self):

        mask_list = numpy.loadtxt(
            builtins.input("Where is the custom mask text file? ")
        )

        with open(builtins.input("Where should the new file be saved? "),
                'w+') as mkOut:
            for n in range(self.gampList.shape[0]):
                if "gamp" in self.File:
                    mk_event = self.gampT.writeEvent(self.gampList[n,:,:])
                    if float(mask_list[n]) == 1.0:
                        mk_event.writeGamp(mkOut)
                if "txt" in self.File:
                    if float(self.mkList[n]) == 1.0:
                        mk_event = self.gampList[n]
                        for i in mk_event.keys():
                            if len(mk_event) > 1:
                                mkOut.write(str(i)+"="+str(mk_event.pop(i))+",")
                            elif len(mk_event) == 1:
                                mkOut.write(str(i)+"="+str(mk_event.pop(i))+"\n")


parser = argparse.ArgumentParser(
    description="A tool for producing gamp files from phase space using "
                "pre-calculated mask files."
)

parser.add_argument(
    "file",
    help="The full filepath/name of the gamp or text file to be masked.",
    default=""
)

parser.add_argument(
    "-pf", "--acceptance_mask",
    help="The full filepath/name of the pf acceptance (.txt) file to use.",
    default=""
)

parser.add_argument(
    "-pfOut", "--accepted_out",
    help="The full filepath/name of the accepted output file.",
    default="./pf_Out"
)

parser.add_argument(
    "-w", "--weighted_mask",
    help="The full filepath/name of the weight mask (.npy) file to use.",
    default=""
)

parser.add_argument(
    "-wOut", "--weighted_out",
    help="The full filepath/name of the weighted output file.",
    default="./weight_Out"
)

parser.add_argument(
    "-b", "--both_masks",
    help="Use both the acceptance and weighted masks.",
    action="store_true"
)

parser.add_argument(
    "-bOut", "--both_out",
    help="The full filepath/name of the accepted and weighted output file.",
    default="./acc_weight_Out"
)

parser.add_argument(
    "-c", "--custom_mask",
    help="Use a custom mask.",
    action="store_true"
)

args = parser.parse_args()

gM = GampMasker(file=args.file,pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.acceptance_mask != "":
    if args.accepted_out != "":
        print("masking pf!")
        gM.maskPF()
    else:
        print("Need a filepath to save new accepted file to.")
        sys.exit()


gM = GampMasker(file=args.file,pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.weighted_mask != "":
    if args.weighted_out != "":
        print("masking wn!")
        gM.maskWN()
    else:
        print("Need a filepath to save new weighted file to.")
        sys.exit()

gM = GampMasker(file=args.file,pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.both_masks:
    if args.accepted_out != "":
        if args.weighted_out != "":
            print("masking both!")
            gM.maskBoth()
        else:
            print("Need a filepath to save new weighted file to.")
            sys.exit()

    else:
        print("Need a filepath to save new accepted file to.")
        sys.exit()


gM = GampMasker(file=args.file,pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.custom_mask:
    print("masking any!")
    gM.maskAny()

