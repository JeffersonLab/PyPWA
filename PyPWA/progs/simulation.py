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

"""
Entry Point for Simulate
"""

import argparse
import copy
import logging
import multiprocessing
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as npy
import yaml

from PyPWA import info as _info
from PyPWA.libs import configuration
from PyPWA.libs import function
from PyPWA.libs import simulate
from PyPWA.libs.file import project, processor

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


_LOGGER = logging.getLogger(__file__)

# Function, Intensity, Setup,
# Parameters,
# Data, Slot Name, Output, Enable Cache
_SETTINGS = Tuple[
    Path, str, str,
    Dict[str, npy.float64],
    Path, str, Path, bool
]

_EXAMPLE = {
    "Version": 1,
    "Processes": multiprocessing.cpu_count(),
    "Function": {
        "Path": 'function.py',
        "Intensity Name": "intensity",
        "Setup Name": "setup"
    },

    "Parameters": {
        "A1": 1,
        "A2": 2,
        "A3": 3.1
    },

    "Data": {
        "Path": "data.type",
        "Folder": "folder_name_if_table remove if not using tables.",
        "Output": "output.txt remove if using tables"
    }
}

_TEMPLATE = {
    "Version": int,
    "Processes": int,
    "Function": {
        "Path": str,
        "Intensity Name": str,
        "Setup Name": str
    },
    "Parameters": dict(),
    "Data": {
        "Path": str,
        "Slot": str,
        "Output": str
    }
}


def simulation(arguments: List[str] = sys.argv[1:]):
    args = _arguments(arguments)

    config = dict()
    if args.type == "config":
        if isinstance(args.config, Path) or args.example:
            config = _handle_configuration(args)  # Will exit if printing config
        else:
            print("Try 'pysimulate config --help")
            sys.exit(1)

    print("Parsing provided parameters")
    function_path, intensity_name, setup_name, \
        parameters, data_path, folder_name, output, use_cache = \
        _process_arguments(config, args)

    print("Loading data")
    if folder_name:
        factory = project.ProjectDatabase(data_path, "r")
        data = factory.get_folder(folder_name)

    else:
        data = processor.DataProcessor(use_cache).parse(data_path)

    print("Loading functions")
    try:
        intensity = function.load(function_path, intensity_name)
    except ImportError as error:
        print("Failed to load the intensity function!")
        raise error

    try:
        setup = function.load(function_path, setup_name)
    except ImportError as error:
        print("Failed to load the setup function!")
        raise error

    print("Starting Simulation")
    rejection = simulate.monte_carlo_simulation(
        intensity, setup, parameters, data
    )

    if folder_name:
        data.data.add_data(data.data.PASSFAIL, rejection)

    if output:
        processor.DataProcessor().write(output, rejection)

    if not folder_name and not output:
        _LOGGER.warn("No output was provided! Using stdout for output!")
        [print(int(x)) for x in rejection]


def _arguments(args: List[str]) -> argparse.ArgumentParser.parse_args:
    arguments = argparse.ArgumentParser()

    subparsers = arguments.add_subparsers(dest="type")

    config_subparser = subparsers.add_parser("config")

    config_subparser.add_argument(
        "config", type=Path, nargs="?",
        help="Use settings from a pre-made configuration file"
    )

    config_subparser.add_argument(
        "--example", action="store_true",
        help="Print an example configuration for PySimulate"
    )

    arguments.add_argument(
        "--data", type=Path, metavar="DATA_FILE",
        help="Data File or table to use for simulation"
    )

    arguments.add_argument(
        "--output", type=Path, metavar="OUTPUT_FILE",
        help="File to right rejection list out too, "
             "omit if you are using tables"
    )

    arguments.add_argument(
        "--folder", metavar="FOLDER_NAME",
        help="The name of the slot to load from in the table. Omitted if not"
             " using a table."
    )

    arguments.add_argument(
        "--disable_cache", action="store_true",
        help="Disable caching when loading data from a file."
    )

    arguments.add_argument(
        "--param", "-p", nargs=2, action="append", metavar=("NAME", "VALUE"),
        help="Parameters to simulate with, as: parameter_name value"
    )

    arguments.add_argument(
        "--function", metavar="PYTHON_FILE", type=Path,
        help="Python source file containing the functions for intensity for "
             "the simulation"
    )

    arguments.add_argument(
        "--intensity", metavar="INTENSITY_NAME", default="intensity",
        help="Name of the intensity function inside the source file."
    )

    arguments.add_argument(
        "--setup", metavar="SETUP_NAME", default="setup",
        help="Name of the setup function inside the source file"
    )

    return arguments.parse_args(args)


def _handle_configuration(args: argparse.Namespace) -> Dict[str, Any]:

    if args.example:
        if args.config:
            configuration.write(args.config, _EXAMPLE)
        else:
            print(yaml.dump(_EXAMPLE))
        sys.exit()

    if args.config.exists():
        return configuration.parse(args.config, _TEMPLATE)
    else:
        raise ValueError(f"{args.conf.name} doesn't exist!")


def _process_arguments(
        config: Dict[str, Any], args: argparse.Namespace) -> _SETTINGS:
    """Extracts information from both arguments and configuration file


    Layout
    ------
    - Fill out Dictionary
    - Convert strings to paths
    - Replace values with provided arguments
    - Set extra variables
    - Handle KeyErrors with specific values that don't have defaults
    """
    combined = copy.deepcopy(config)

    # Fill in root keys in dictionary if not provided
    if "Data" not in combined:
        combined["Data"] = dict()

    if "Function" not in combined:
        combined["Function"] = dict()

    if "Parameters" not in combined:
        combined["Parameters"] = dict()
    else:
        for key in combined["Parameters"]:
            combined["Parameters"][key] = npy.float(combined["Parameters"][key])

    # Convert str to Path, if in configuration file
    if "Path" in combined["Data"]:
        combined["Data"]["Path"] = Path(combined["Data"]["Path"])
        combined["Data"]["Path"] = combined["Data"]["Path"].resolve()

    if "Path" in combined["Function"]:
        combined["Function"]["Path"] = Path(combined["Function"]["Path"])

    if "Output" in combined["Data"]:
        combined["Data"]["Output"] = Path(combined["Data"]["Output"])

    # Replace data path if path is provided and exists
    if args.data and args.data.exists():
        combined["Data"]["Path"] = args.data

    # Even if we don't have a slot, the value needs to be set
    if args.folder or "Folder" not in combined["Data"]:
        combined["Data"]["Folder"] = args.folder

    # Replace function path if provided and exists
    if args.function and args.function.exists():
        combined["Function"]["Path"] = args.function

    # Replace output if provided it or set it if unset
    if args.output or "Output" not in combined["Data"]:
        combined["Data"]["Output"] = args.output

    # Replace intensity name if provided it or set it if unset
    if "Intensity Name" not in combined["Function"] or (
            "Intensity Name" in combined["Function"] and
            args.intensity != "intensity"):
        combined["Function"]["Intensity Name"] = args.intensity

    # Replace setup name if provided it or set it if unset
    if "Setup Name" not in combined["Function"] or (
            "Setup Name" in combined["Function"] and
            args.setup != "setup"):
        combined["Function"]["Setup Name"] = args.setup

    # Append provided parameters
    if args.param:
        for param in args.param:
            combined["Parameters"][param[0]] = npy.float(param[1])

    # Set caching variable
    combined["Data"]["Cache"] = args.disable_cache

    # We only check the values that don't have defaults and have to be set
    try:
        func_path = combined["Function"]["Path"]
    except KeyError:
        print(
            "You must provide a function path either directly or in the"
            " configuration file"
        )
        sys.exit(126)

    try:
        data_path = combined["Data"]["Path"]
    except KeyError:
        print(
            "You must provide a path to the data either directly or in the"
            " configuration file"
        )
        sys.exit(126)

    return (
        func_path, combined["Function"]["Intensity Name"],
        combined["Function"]["Setup Name"], combined["Parameters"],
        data_path, combined["Data"]["Folder"], combined["Data"]["Output"],
        combined["Data"]["Cache"]
    )
