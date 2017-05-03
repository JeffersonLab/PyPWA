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
The nestle maximizer
--------------------
This is a complex maximizer that takes a random array of n dimensions and 
passes it through the prior to generate point data, then moves the live 
points depending on the results of the returned value. To know what each 
option does, check the actual documentation for nestle on ReadTheDocs.io or 
the documentation inside nestle.

- _graph_data - Doesn't graph the data, but saves the data needed to 
  generate a graph to file.

- _save_results - Where the table for the results are created and the data
  is saved to disk

- _setup - Provides the interface between the plugin and the configurator.

- nested - Where the actual optimization process takes place.
"""


from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.nestle import _setup
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class NestleOptions(options.Plugin):
    plugin_name = "Nestle"
    setup = _setup.NestleSetup
    provides = options.Types.OPTIMIZER
    defined_function = _setup.NestlePriorFunction
    module_comment = "Nestle, a python based multinest implementation."

    default_options = {
        "prior location": "/location/to/prior.py",
        "prior name": "prior_function",
        "folder location": None,
        "ndim": 1,
        "npoints": 100,
        "method": "single",
        "update interval": None,
        "npdim": None,
        "maxiter": None,
        "maxcall": None,
        "dlogz": None,
        "decline_factor": None
    }
    option_difficulties = {
        "prior location": options.Levels.REQUIRED,
        "prior name": options.Levels.REQUIRED,
        "folder location": options.Levels.OPTIONAL,
        "ndim": options.Levels.REQUIRED,
        "npoints": options.Levels.OPTIONAL,
        "method": options.Levels.OPTIONAL,
        "update interval": options.Levels.ADVANCED,
        "npdim": options.Levels.ADVANCED,
        "maxiter": options.Levels.ADVANCED,
        "maxcall": options.Levels.ADVANCED,
        "dlogz": options.Levels.ADVANCED,
        "decline_factor": options.Levels.ADVANCED
    }

    option_types = {
        "prior location": str,
        "prior name": str,
        "folder location": str,
        "ndim": int,
        "npoints": int,
        "method": ["classic", "single", "multi"],
        "update interval": int,
        "npdim": int,
        "maxiter": int,
        "maxcall": int,
        "dlogz": float,
        "decline_factor": float
    }

    option_comments = {
        "prior location":
            "The path of the file containing the prior.",
        "prior name":
            "The name of the prior function.",
        "folder location":
            "The name of the folder where you want to save graph data into.",
        "ndim":
            "Number of parameters returned by prior.",
        "npoints":
            "Number of active points.",
        "method":
            "Method to select new points.",
        "update interval":
            "Only update the new point selector every "
            "``update_interval``-th likelihood call.",
        "npdim":
            "Number of parameters accepted by prior.",
        "maxiter":
            "Maximum number of iterations.",
        "maxcall":
            "Maximum number of likelihood evaluations.",
        "dlogz":
            "If supplied, iteration will stop when the estimated "
            "contribution of the remaining prior volume to the total "
            "evidence falls below this threshold.",
        "decline_factor":
            "If supplied, iteration will stop when the weight of newly "
            "saved samples has been declining for x consecutive samples."
    }
