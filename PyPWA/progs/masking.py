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


from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

import numpy as npy
import tqdm

from PyPWA.libs.file import processor
from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def start_masking(arguments: List[str] = sys.argv[1:]):
    args = _arguments(arguments)
    file_manager = processor.DataProcessor(False)

    # Load the input file
    if args.input.exists():
        input_file = file_manager.get_reader(args.input)
        output_file = file_manager.get_writer(args.output, input_file.data_type)
    else:
        print(f"{args.input} must exist!")
        return 1

    # Load the correct file
    if args.use_or:
        logic = npy.logical_or
    elif args.use_xor:
        logic = npy.logical_xor
    elif args.use_or and args.use_xor:
        print("Only select OR or XOR, not both!")
        return 1
    else:
        logic = npy.logical_and

    # Setup progress bar for mask files
    if len(args.mask) > 1:
        disable = False
    else:
        disable = True

    # Merge together masks
    pf = None
    for mask_file in tqdm.tqdm(args.mask, disable=disable):  # type: Path
        if mask_file.exists():
            current_pf = file_manager.parse(mask_file)
        else:
            print(f"{mask_file} must exist!")
            return 1

        # Convert selection array to a boolean mask.
        if "u8" == current_pf.dtype or "u4" == current_pf.dtype:
            new_pf = npy.zeros(len(input_file), bool)
            new_pf[current_pf] = True
            current_pf = new_pf

        if isinstance(pf, type(None)):
            pf = current_pf
        else:
            pf = logic(pf, current_pf)

    # Handle no masks provided
    if isinstance(pf, type(None)):
        pf = npy.ones(len(input_file), bool)

    if len(pf) != len(input_file):
        print(
            f"Masking data isn't the same length as input!"
            f" Mask is {len(pf)} and input is {len(input_file)}."
        )
        return 1

    # Setup description
    if pf.all() == 1:
        description = "Converting:"
    else:
        description = "Masking:"

    # Input masked to output
    progress = tqdm.tqdm(
        zip(pf, input_file), total=len(pf), unit="Events",
        desc=description
    )
    for do_write, event in progress:
        if do_write:
            output_file.write(event)

    input_file.close()
    output_file.close()


def _arguments(args: List[str]) -> argparse.ArgumentParser.parse_args:
    arguments = argparse.ArgumentParser()

    arguments.add_argument(
        "--input", "-i", type=Path, required=True,
        help="The source file, or the file you want to mask."
    )

    arguments.add_argument(
        "--output", "-o", type=Path, required=True,
        help="The destination file."
    )

    arguments.add_argument(
        "--mask", "-m", type=Path, action="append",
        help="The masking files, can be either .pf or .sel"
    )

    arguments.add_argument(
        "--use_or", action="store_true",
        help="OR mask files together instead of AND"
    )

    arguments.add_argument(
        "--use_xor", action="store_true",
        help="XOR mask files together instead of AND"
    )

    return arguments.parse_args(args)
