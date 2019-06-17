#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import binning
from PyPWA.libs.file import slot_table

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def start_binning():
    results = _arguments()
    metadata_file = Path(results.file.stem + "_bin_queue.json")

    # Parse pre-existing queue if it exists
    if metadata_file.exists():
        try:
            metadata = json.load(metadata_file.open())
        except json.JSONDecodeError:
            metadata = dict()
            print("JSON Failed to parse")
    else:
        metadata = dict()

    # Removes all stored metadata
    if results.clear:
        metadata = dict()
        metadata_file.unlink()

    # Add another bin to the queue
    if results.type:
        metadata = _add_to_queue(metadata, results)
        with metadata_file.open("w") as stream:
            json.dump(metadata, stream)

    # Load the main table and slot
    table = slot_table.SlotFactory(results.file, "a")
    slot = table.get_slot(results.slot)

    # Setup the binned data slot
    binned_slot = binning.BinSlot(slot)
    table.set_custom_slot(binned_slot)

    # Actually bin the data
    if results.execute:
        bf = binning.BinFactory(slot)

        for key in metadata.keys():
            bf.add_fixed_range(
                binning.BinType(metadata[key]["variable"]),
                metadata[key]["lower"], metadata[key]["upper"],
                metadata[key]["num"]
            )

        bf.execute()
        binned_slot.bin(bf.produced_truth_table)

    # Write out the data to a directory if requested.
    if results.make_dirs:
        binned_slot.slot_to_folder()


def _arguments() -> argparse.ArgumentParser.parse_args:
    arguments = argparse.ArgumentParser()

    arguments.add_argument(
        "file", type=Path, help="Name of the HDF5 table."
    )

    arguments.add_argument(
        "slot", type=str, help="Name of the dataset"
    )

    arguments.add_argument(
        "--clear", "-c", action="store_true",
        help="Clears the queue"
    )

    arguments.add_argument(
        "--execute", "-e", action="store_true",
        help="Bins out the data using the queued parameters"
    )

    arguments.add_argument(
        "--make-dirs", "-d", action="store_true",
        help="Output the binned data into a bin_data directory"
    )

    bin_subparsers = arguments.add_subparsers(dest="type")

    # Range
    bin_range = bin_subparsers.add_parser(
        "range", help="Queues a bin using variable ranges"
    )

    bin_range.add_argument(
        "--variable", "-v", type=str, required=True,
        help="The variable to use for binning. t, tprime, mass, and "
             "beam are supported"
    )

    bin_range.add_argument(
        "--lower-limit", "-l", type=float, required=True,
        help="Specifies the lower limit of the bins"
    )

    bin_range.add_argument(
        "--number-of-bins", "-n", type=int, required=True,
        help="Specifies the number of bins to create"
    )

    bin_range.add_argument(
        "--upper-limit", "-u", type=float, required=True,
        help="Defines the range of each bin"
    )

    return arguments.parse_args()


def _add_to_queue(
        metadata: Dict[str, Dict[str, Any]],
        results: argparse.Namespace) -> Dict[str, Dict[str, Any]]:
    if results.variable.lower() == "mass":
        variable = "mass"
    elif results.variable.lower() == "t":
        variable = "t"
    elif results.variable.lower() in ("tprime", "t_prime", "t-prime"):
        variable = "tp"
    elif results.variable.lower() == "beam":
        variable = "beam"
    else:
        raise ValueError(f"Unknown variable {results.variable}!")

    if results.type == "range":
        new_index = str(len(metadata.keys()))
        metadata[new_index] = {
            "variable": variable,
            "lower": results.lower_limit,
            "upper": results.upper_limit,
            "num": results.number_of_bins
        }

    return metadata

