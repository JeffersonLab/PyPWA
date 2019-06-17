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
from pathlib import Path
from typing import List, Optional as Opt

from tqdm import tqdm

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.file import slot_table
from PyPWA.libs.file.processor import DataProcessor

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def data():
    results = _arguments()
    table = slot_table.SlotFactory(results.file, "a")

    # If a new slot, process the primary data
    if results.slot not in table.slots:
        _process_primary_data(table, results.slot, results.primary)

    # Process the extras
    slot = table.get_slot(results.slot)
    _process_extra_data(slot, results.extra)


def _arguments() -> argparse.ArgumentParser.parse_args:
    arguments = argparse.ArgumentParser()

    arguments.add_argument(
        "file", type=Path, help="Name of the HDF5 table."
    )

    arguments.add_argument(
        "slot", type=str, help="Name of the dataset"
    )

    arguments.add_argument(
        "--primary", "-p", type=Path,
        help="Primary data for the dataset, IE Gamp data"
    )

    arguments.add_argument(
        "--extra", "-e", type=Path, nargs="*",
        help="Any extra data to add to the dataset."
    )

    return arguments.parse_args()


def _process_primary_data(table: slot_table.SlotFactory,
                          slot_name: str, primary: Path):
    if not primary:
        raise RuntimeError("Primary must be provided with new slots")

    read = DataProcessor().get_reader(primary)
    table.add_slot(slot_name, read.fields, read.is_particle_pool, len(read))
    slot = table.get_slot(slot_name)

    for event in tqdm(read):
        slot.root_append(event)
    slot.flush()


def _process_extra_data(slot: slot_table.DataSlot, extras: Opt[List[Path]]):
    dp = DataProcessor()

    if not extras:
        return

    for extra in tqdm(extras):
        array = dp.parse(extra)
        slot.add_data(extra.stem, array)
