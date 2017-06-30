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
Package for PySimulate, GenerateIntensities, and GenerateWeights
----------------------------------------------------------------
PySimulate is used to generate simulated data for a amplitude using a flat 
plane of data provided by the user.

- _libs - where the actual logic of the program is defined.

- _processing - contains the objects required to interface with a Kernel 
  Processing package.

- initial_setup - where the Setup object is defined for the Configurator to 
  interface with PySimulate properly.

- simulate - where the 'main' object is, though all it does it route
  information between the various objects defined in _libs.py
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.progs.shell import pyshell_functions
from PyPWA.progs.shell.simulate import initial_setup

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ShellSimulation(options.Main):

    plugin_name = "shell simulation"
    setup = initial_setup.SimulationSetup
    defined_function = pyshell_functions.ShellFunctionFile

    required_plugins = [
        options.Types.DATA_PARSER,
        options.Types.KERNEL_PROCESSING
    ]

    module_comment = "A Python Statistical Simulation Tool"

    option_comments = {
        "the type":
            "If you are seeing this, something went very wrong.",
        "function's location":
            "The path to the intensity function.",
        "processing name": "The name of the intensity function.",
        "setup name": "The name of the setup function.",
        "data location": "The path to your data.",
        "parameters": "The parameters to simulate against.",
        "max intensity":
            "The largest intensity in your entire data set",
        "save name": "The name to use for saving data."
    }

    default_options = {
        "the type": "full",
        "function's location": "/path/to/the/function.py",
        "processing name": "processing_function",
        "setup name": "setup_function",
        "data location": "/path/to/the/data.csv",
        "parameters": {"A1": 1, "A2": 2, "A3": 0.1, "A4": -10.0001},
        "max intensity": "2.123123",
        "save name": "output"
    }

    option_difficulties = {
        "the type": options.Levels.REQUIRED,
        "function's location": options.Levels.REQUIRED,
        "processing name": options.Levels.REQUIRED,
        "setup name": options.Levels.REQUIRED,
        "data location": options.Levels.REQUIRED,
        "parameters": options.Levels.REQUIRED,
        "max intensity": options.Levels.REQUIRED,
        "save name": options.Levels.REQUIRED
    }

    option_types = {
        "the type": ["full", "intensities", "weighting"],
        "function's location": str,
        "processing name": str,
        "setup name": str,
        "data location": str,
        "parameters": dict,
        "max intensity": float,
        "save name": str
    }
