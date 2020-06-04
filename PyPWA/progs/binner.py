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

import tqdm
import argparse
import sys
from pathlib import Path
from typing import List

import yaml

from PyPWA.libs.file import project, processor
from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


CONFIGURATION = {
    "version": 1,
    "primary data": "raw_events.gamp",
    "binned data": [
        "example.pf",
        "qfactor.txt"
    ],
    "binning settings": {
        0: {
            "type": "range",
            "variable": "mass",
            "lower limit": .1,
            "upper limit": .5,
            "count": 10
        },
        1: {
            "type": "fixed",
            "variable": "t",
            "count": 1500
        }
    }
}


def start_binning(arguments: List[str] = sys.argv[1:]):
    table = Path("binning.hd5")
    parser = processor.DataProcessor()
    base_dir = Path("bin_data")
    args = _arguments(arguments)

    if args.example:
        print(yaml.dump(CONFIGURATION))
        sys.exit(0)

    if not args.configuration:
        print("You must provide a configuration file!")
        sys.exit(1)

    with open(args.configuration) as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    if base_dir.exists():
        print(f"Please delete {base_dir} first before running.")
        sys.exit(1)

    if table.exists():
        table.unlink()

    root_data = parser.get_reader(config["primary data"])

    # Calculate total space requirements
    event_count = root_data.get_event_count()
    num_bins = 1
    for value in config["binning settings"].values():
        if value["type"] == "range":
            num_bins *= value["count"] + 2
        else:
            num_bins += value["count"]

    space = (num_bins * root_data.get_event_count())
    space += root_data.input_path.stat().st_size

    if config["binned data"]:
        for file in config["binned data"]:
            space += Path(file).stat().st_size

    space /= 1000000000  # Bytes to Gigabytes

    print(f"Estimated to take {space:.2f}Gb of disk space")

    folder_manager = project.ProjectDatabase(table, "w")
    folder = folder_manager.make_folder(
        "binning_data", root_data, config["primary data"], True
    )

    if config["binned data"]:
        pbar = tqdm.tqdm(
            total=len(config["binned data"]), unit="file",
            desc="Parsing binned data"
        )
        for file in config["binned data"]:
            pbar.set_postfix_str(f"file={file}")
            data = parser.parse(file)
            folder.unmanaged.add(file.replace(".", "_"), data, file)
            pbar.update(1)
        pbar.close()

    for setting_index in config["binning settings"].keys():
        settings = config["binning settings"][setting_index]

        # Convert configuration to variable
        if settings["variable"] == "mass":
            var = folder.binning.BinVars.MASS
        elif settings["variable"] == "beam":
            var = folder.binning.BinVars.BEAM
        elif settings["variable"] == "t":
            var = folder.binning.BinVars.T
        elif settings["variable"] == "tprime":
            var = folder.binning.BinVars.T_PRIME
        else:
            print(
                f"{settings['variable']} variable not understood in "
                f"{setting_index}!"
            )
            sys.exit(1)

        # Queue the binning parameters
        if settings["type"] == "range":
            folder.binning.add_fixed_range(
                var, settings["lower limit"],
                settings["upper limit"], settings["count"]
            )
        elif settings["type"] == "fixed":
            folder.binning.add_fixed_count(
                var, settings["count"]
            )
        else:
            print(
                f"{settings['type']} is not understood in "
                f"{setting_index}!"
            )
            sys.exit(1)

    folder.binning.execute()
    _table_to_directory(folder, base_dir)

    folder_manager.close()

    if "clean up" in config:
        if config["clean up"]:
            table.unlink()
    else:
        table.unlink()

    print("\nCompleted!")


def _arguments(args: List[str]) -> argparse.ArgumentParser.parse_args:
    arguments = argparse.ArgumentParser()

    arguments.add_argument(
        "configuration", type=Path, nargs="?"
    )

    arguments.add_argument(
        "--example", "-e", action="store_true"
    )

    return arguments.parse_args(args)


def _table_to_directory(folder, base_dir):
    parser = processor.DataProcessor()
    folder_pbar = tqdm.tqdm(
        folder.binning.get_bin_directory(), unit="folder"
    )
    file_pbar = tqdm.tqdm(
        total=len(folder.unmanaged.nodes) + 1, unit="file"
    )

    folder_pbar.set_description()

    for directory in folder_pbar:
        # Create the new directory for the bin
        file_pbar.reset()
        new_path = base_dir / directory.bin_location
        new_path.mkdir(parents=True)

        root_path = new_path / directory.root.filename

        with parser.get_writer(root_path, directory.root.data_type) as w:
            for event in tqdm.tqdm(
                    directory.root.iterate_data(1),
                    total=len(directory), unit=" event",
                    postfix=f"file={folder.root.filename}", position=2):
                w.write(event)
        file_pbar.update(1)

        for extra_data in directory.unmanaged:
            data_path = new_path / extra_data.filename

            if extra_data.data_type == processor.DataType.STRUCTURED:
                with parser.get_writer(data_path, extra_data.data_type) as w:
                    for event in tqdm.tqdm(
                            extra_data.iterate_data(1), unit="event",
                            total=len(extra_data),
                            postfix=f"file={folder.root.filename}", position=2):
                        w.write(event)
            else:
                parser.write(data_path, extra_data.data)
            file_pbar.update(1)

    folder_pbar.close()
    file_pbar.close()
