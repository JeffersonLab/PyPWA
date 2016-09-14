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
Entry point for console GeneralShell
"""

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.configurator import configurator
from PyPWA.core_libs.wrappers import StartProgram

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


@StartProgram(configurator.Configurator)
def general_fitting(*args):
    description = u"An extremely fitting shell that allows the User" \
                  u"to select their own likelihood and function."
    configuration = {
        "description": description,
        "main": "shell fitting method",
        "main name": "general fitting",
        "extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def likelihood_fitting(*args):
    description = u"Amplitude Fitting using the Likelihood Estimation " \
                  u"Method."
    configuration = {
        "description": description,
        "main": "shell fitting method",
        "main name": "likelihood fitting",
        "main options": {"type": "likelihood"},
        "extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def chi_squared(*args):
    description = u"Amplitude Fitting using the ChiSquared Method."
    configuration = {
        "description": description,
        "main": "shell fitting method",
        "main name": "chi-squared fitting",
        "main options": {
            "type": "chi-squared",
            "generated length": None,
            "accepted monte carlo location": None
        },
        "extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def simulator(*args):
    description = u"Simulation using the the Acceptance Reject Method."
    configuration = {
        "description": description,
        "main": "shell simulation",
        "main name": "simulator",
        "main options": {"type": "complete"},
        "extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def intensities(*args):
    description = u"Generates the Intensities for Rejection Method."
    configuration = {
        "description": description,
        "main": "shell simulation",
        "main name": "intensities",
        "main options": {"type": "intensities"},
        "extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def rejection_method(*args):
    description = u"Takes generated intensities to run through the " \
                  u"Rejection Method."
    configuration = {
        "description": description,
        "main": "shell simulation",
        "main name": "rejection method",
        "main options": {"type": "rejection"},
        "extras": args
    }
    return configuration
