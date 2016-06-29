#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A Minor rewrite of GampMasker
"""


import argparse
import os
import sys
import fileinput

import numpy

from PyPWA.unoptimized.pythonPWA.fileHandlers.gampTranslator import \
    gampTranslator

from PyPWA import VERSION, STATUS, LICENSE

__author__ = ["Joshua Pond"]
__credits__ = ["Joshua Pond", "Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class GampMasker (object):

    def __init__(self, file=None, pf_file=None, wn_file=None):

        self.file = file
        if "gamp" in self.file:
            self.gamp_translator = gampTranslator(self.file)
            if not os.path.isfile(self.file.rstrip(".gamp") + ".npy"):
                numpy.save(
                    self.file.rstrip(".gamp") + ".npy",
                    self.gamp_translator.translate(
                        self.file.rstrip(".gamp") + ".npy"
                    )
                )
            self.gamp_list = numpy.load(self.file.rstrip(".gamp") + ".npy")
        elif "txt" in self.file:
            pass

        self.pf_file = pf_file
        if os.path.isfile(self.pf_file):
            self.pf_list = numpy.loadtxt(self.pf_file)
        else:
            self.pf_list = [0]

        self.wn_file = wn_file
        if os.path.isfile(self.wn_file):
            self.wn_list = numpy.load(self.wn_file)
        else:
            self.wn_list = [0]

    def mask_pf(self):
        with open(args.accepted_out, 'w+')as pfOut:
            if "gamp" in self.file:
                print(self.gamp_list.shape[0])
                for index in range(self.gamp_list.shape[0]):
                    pf_event = self.gamp_translator.writeEvent(
                        self.gamp_list[index, :, :]
                    )
                    if float(self.pf_list[index]) == 1.0:
                        pf_event.writeGamp(pfOut)

            if "txt" in self.file:
                for index, line in enumerate(fileinput.input([self.file])):
                    if float(self.pf_list[index]) == 1.0:
                        pfOut.write(line)

    def mask_wn(self):
        with open(args.weighted_out, 'w+') as wnOut:
            if "gamp" in self.file:
                for index in range(self.gamp_list.shape[0]):
                    wn_event = self.gamp_translator.writeEvent(
                        self.gamp_list[index, :, :]
                    )
                    if float(self.wn_list[index]) == 1.0:
                        wn_event.writeGamp(wnOut)
            if "txt" in self.file:
                for index, line in enumerate(fileinput.input([self.file])):
                    if float(self.wn_list[index]) == 1.0:
                        wnOut.write(line)

    def mask_both(self):
        with open(args.both_out, 'w+') as btOut:
            if "gamp" in self.file:
                for index in range(self.gamp_list.shape[0]):
                    bt_event = self.gamp_translator.writeEvent(
                        self.gamp_list[index, :, :]
                    )
                    if float(self.wn_list[index]) == 1.0 and \
                       float(self.pf_list[index]) == 1.0:
                        bt_event.writeGamp(btOut)
            if "txt" in self.file:
                for index, line in enumerate(fileinput.input([self.file])):
                    if float(self.wn_list[index]) == 1.0 and \
                       float(self.pf_list[index]) == 1.0:
                        btOut.write(line)

    def mask_any(self):

        mask_list = numpy.loadtxt(
            input("Where is the custom mask text file? ")
        )

        with open(input("Where should the new file be saved? "), 'w+') as mkOut:
            for index in range(self.gamp_list.shape[0]):
                if "gamp" in self.file:
                    mk_event = self.gamp_translator.writeEvent(
                        self.gamp_list[index, :, :]
                    )
                    if float(mask_list[index]) == 1.0:
                        mk_event.writeGamp(mkOut)
                if "txt" in self.file:
                    if float(mask_list[index]) == 1.0:
                        mk_event = self.gamp_list[index]
                        for i in mk_event.keys():
                            if len(mk_event) > 1:
                                mkOut.write(
                                    str(i) + "=" + str(mk_event.pop(i)) + ","
                                )
                            elif len(mk_event) == 1:
                                mkOut.write(
                                    str(i) + "=" + str(mk_event.pop(i)) + "\n"
                                )


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

gM = GampMasker(file=args.file, pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.acceptance_mask != "":
    if args.accepted_out != "":
        print("masking pf!")
        gM.mask_pf()
    else:
        print("Need a filepath to save new accepted file to.")
        sys.exit()


gM = GampMasker(file=args.file, pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.weighted_mask != "":
    if args.weighted_out != "":
        print("masking wn!")
        gM.mask_wn()
    else:
        print("Need a filepath to save new weighted file to.")
        sys.exit()

gM = GampMasker(file=args.file, pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.both_masks:
    if args.accepted_out != "":
        if args.weighted_out != "":
            print("masking both!")
            gM.mask_both()
        else:
            print("Need a filepath to save new weighted file to.")
            sys.exit()

    else:
        print("Need a filepath to save new accepted file to.")
        sys.exit()


gM = GampMasker(file=args.file, pf_file=args.acceptance_mask,
                wn_file=args.weighted_mask)

if args.custom_mask:
    print("masking any!")
    gM.mask_any()
