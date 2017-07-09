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
PyFit, LikelihoodFitting, and ChiSquaredFitting
-----------------------------------------------
PyFit is a simple fitting tool that can use multiple processes depending on
the processing module that is picked.

- likelihoods - the various builtin likelihoods the PyFit supports.

- _processing_interface - PyFits interface with the processing package, also
  handles the output mechanism in a second thread.

- interfaces - the interfaces that need to be extended to define a new
  likelihood function.

- initial_setup - how the configurator package interfaces the PyFit
  Main object.

- fit - the main object and the likelihood loading object are contained.
"""

from PyPWA.progs.shell.fit import intial_setup

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator import options
from PyPWA.progs.shell import pyshell_functions
from PyPWA.progs.shell.fit import pyfit

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ShellFitting(options.Main):

    __likelihood_loader = pyfit.LikelihoodPackager()

    plugin_name = "shell fitting method"
    setup = intial_setup.FittingSetup
    defined_function = pyshell_functions.ShellFunctionFile
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
        "qfactor location": None,
        "data location": "/path/to/the/data.csv",
        "internal data": {"quality factor": "Qfactors"},
        "accepted monte carlo location": None,
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
        "internal data": options.Levels.OPTIONAL,
        "accepted monte carlo location": options.Levels.OPTIONAL,
        "save name": options.Levels.REQUIRED
    }

    option_types = {
        "likelihood type": __likelihood_loader.get_likelihood_name_list(),
        "generated length": int,
        "function's location": str,
        "processing name": str,
        "setup name": str,
        "qfactor location": str,
        "data location": str,
        "internal data": {
            "quality factor": str,
            "binned data": str,
            "event errors": str,
            "expected values": str
        },
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
        "internal data": "Internal name mapping.",
        "accepted monte carlo location":
            "The path to your accepted monte carlo file",
        "save name": "The name out the output files."
    }
