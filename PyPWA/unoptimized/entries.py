import argparse
import sys

from PyPWA.unoptimized.gampMasker import GampMasker


def gamp_masker_entry():
    parser = argparse.ArgumentParser(
        description="A tool for producing gamp files from phase space "
                    "using pre-calculated mask files."
    )

    parser.add_argument(
        "file",
        help="The full filepath/name of the gamp or text file to be "
             "masked.",
        default=""
    )

    parser.add_argument(
        "-pf", "--acceptance_mask",
        help="The full filepath/name of the pf acceptance (.txt) file to "
             "use.",
        default=""
    )

    parser.add_argument(
        "-pfOut", "--accepted_out",
        help="The full filepath/name of the accepted output file.",
        default="./pf_Out"
    )

    parser.add_argument(
        "-w", "--weighted_mask",
        help="The full filepath/name of the weight mask (.npy) file to "
             "use.",
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
        help="The full filepath/name of the accepted and weighted output "
             "file.",
        default="./acc_weight_Out"
    )

    parser.add_argument(
        "-c", "--custom_mask",
        help="Use a custom mask.",
        action="store_true"
    )

    args = parser.parse_args()

    masker = GampMasker(file=args.file, pf_file=args.acceptance_mask,
                        wn_file=args.weighted_mask)

    if args.acceptance_mask != "":
        if args.accepted_out != "":
            print("masking pf!")
            masker.mask_pf()
        else:
            print("Need a filepath to save new accepted file to.")
            sys.exit()

    if args.weighted_mask != "":
        if args.weighted_out != "":
            print("masking wn!")
            masker.mask_wn()
        else:
            print("Need a filepath to save new weighted file to.")
            sys.exit()

    if args.both_masks:
        if args.accepted_out != "":
            if args.weighted_out != "":
                print("masking both!")
                masker.mask_both()
            else:
                print("Need a filepath to save new weighted file to.")
                sys.exit()

        else:
            print("Need a filepath to save new accepted file to.")
            sys.exit()

    if args.custom_mask:
        print("masking any!")
        masker.mask_any()
