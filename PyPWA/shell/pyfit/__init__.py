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
PyFit is a simple fitting tool that can use multiple processes depending on 
the processing module tha is picked.

likelihoods contains the various builtin likelihoods the PyFit supports.

_processing_interface defines PyFits interface with the processing package.

interfaces defines the interfaces that need to be extended to define a new 
likelihood function.

initial_setup defines how the configurator package interfaces the PyFit 
Main object.

pyfit is where the main object and the likelihood loading object are 
contained.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.shell.pyfit import intial_setup

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ShellFitting(options.Main):

    plugin_name = "shell pyfit method"
    setup = intial_setup.FittingSetup
    required_plugins = [
        options.Types.OPTIMIZER,
        options.Types.DATA_PARSER,
        options.Types.KERNEL_PROCESSING
    ]

    default_options = {
        "likelihood type": "likelihood",
        "generated length": 10000,
        "function's location": "/path/to/the/function.py",
        "processing name": "processing_function",
        "setup name": "setup_function",
        "qfactor location": "/path/to/the/data.csv",
        "data location": "/path/to/the/data.csv",
        "accepted monte carlo location": "/path/to/monte/carlo.csv",
        "save name": "output"
    }

    option_difficulties = {
        "likelihood type": options.Levels.REQUIRED,
        "generated length": options.Levels.OPTIONAL,
        "function's location": options.Levels.REQUIRED,
        "processing name": options.Levels.REQUIRED,
        "setup name": options.Levels.REQUIRED,
        "qfactor location": options.Levels.OPTIONAL,
        "data location": options.Levels.REQUIRED,
        "accepted monte carlo location": options.Levels.OPTIONAL,
        "save name": options.Levels.REQUIRED
    }

    option_types = {
        "likelihood type": ["likelihood", "chi-squared"],
        "generated length": int,
        "function's location": str,
        "processing name": str,
        "setup name": str,
        "qfactor location": str,
        "data location": str,
        "accepted monte carlo location": str,
        "save name": str
    }

    module_comment = "PyFit, a simple python data analysis tool."
    option_comments = {
        "likelihood type":
            "Likelihood to use: Chi-Squared, Likelihood, or Empty",
        "generated length": "The number of generated events",
        "function's location": "The path of your functions file",
        "processing name": "The name of your processing function.",
        "setup name": "The name of your setup function.",
        "qfactor location": "The path of the qfactors file.",
        "data location": "The path of your data file.",
        "accepted monte carlo location":
            "The path to your accepted monte carlo file",
        "save name": "The name out the output files."
    }
