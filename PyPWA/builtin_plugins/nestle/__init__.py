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
from PyPWA.builtin_plugins.nestle import nested, _setup
from PyPWA.libs.components.optimizers import opt_plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class NestleOptions(opt_plugins.OptimizerConf, opt_plugins.HasPrior):

    def __init__(self):
        self.name = "nestle"
        self.optimizer_summary = "Nestle, a python based multinest " \
                                 "implementation."

    def get_optimizer_type(self):
        return opt_plugins.Type.MAXIMIZER

    def get_optimizer_parser(self):
        return nested.NestleParserObject()

    def get_optimizer(self):
        return nested.NestledSampling()

    def get_defaults(self):
        return {
            "prior location": "/location/to/prior.py",
            "prior name": "prior_function",
            "ndim": 1,
            "npoints": 100,
            "method": "single",
            "update interval": None,
            "npdim": None,
            "maxiter": None,
            "maxcall": None,
            "dlogz": None,
            "decline factor": None
        }

    def get_difficulties(self):
        return {
            "prior location": opt_plugins.Levels.REQUIRED,
            "prior name": opt_plugins.Levels.REQUIRED,
            "folder location": opt_plugins.Levels.OPTIONAL,
            "ndim": opt_plugins.Levels.REQUIRED,
            "npoints": opt_plugins.Levels.OPTIONAL,
            "method": opt_plugins.Levels.OPTIONAL,
            "update interval": opt_plugins.Levels.ADVANCED,
            "npdim": opt_plugins.Levels.ADVANCED,
            "maxiter": opt_plugins.Levels.ADVANCED,
            "maxcall": opt_plugins.Levels.ADVANCED,
            "dlogz": opt_plugins.Levels.ADVANCED,
            "decline factor": opt_plugins.Levels.ADVANCED
        }

    def get_types(self):
        return {
            "prior location": str,
            "prior name": str,
            "ndim": int,
            "npoints": int,
            "method": ["classic", "single", "multi"],
            "update interval": int,
            "npdim": int,
            "maxiter": int,
            "maxcall": int,
            "dlogz": float,
            "decline factor": float
        }

    def get_option_comments(self):
        return {
            "prior location":
                "The path of the file containing the prior.",
            "prior name":
                "The name of the prior function.",
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
            "decline factor":
                "If supplied, iteration will stop when the weight of newly "
                "saved samples has been declining for x consecutive samples."
        }

    def get_prior_function_template(self):
        return _setup.NestlePriorFunction
