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
from PyPWA.configurator.wrappers import StartProgram
from PyPWA.configurator import configurator

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


@StartProgram(configurator.Configurator)
def likelihood_fitting(*args):
    description = u"Amplitude Fitting using the Likelihood Estimation " \
                  u"Method."
    configuration = {
        "Description": description,
        "main": "shell fitting",
        "kernel plugin": "Builtin Multiprocessing",
        "data plugin": "Builtin Parser",
        "Extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def simulator(*args):
    description = u"Simulation using the the Acceptance Reject Method"
    configuration = {
        "Description": description,
        "main": "shell simulation",
        "options": "simulation = main",
        "kernel plugin": "Builtin Multiprocessing",
        "data plugin": "Builtin Parser",
        "Extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def intensities(*args):
    description = u"Generates the Intensities for Rejection Method"
    configuration = {
        "Description": description,
        "main": "shell simulation",
        "options": "simulation = intensities",
        "kernel plugin": "Builtin Multiprocessing",
        "data plugin": "Builtin Parser",
        "Extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def rejection_method(*args):
    description = u"Takes generated intensities to run through the " \
                  u"Rejection Method"
    configuration = {
        "Description": description,
        "main": "shell simulation",
        "options": "simulation = rejection",
        "kernel plugin": "Builtin Multiprocessing",
        "data plugin": "Builtin Parser",
        "Extras": args
    }
    return configuration


@StartProgram(configurator.Configurator)
def chi_squared(*args):
    description = u"Amplitude Fitting using the ChiSquared Method"
    configuration = {
        "Description": description,
        "main": "shell fitting",
        "options": "likelihood = ChiSquared",
        "kernel plugin": "Builtin Multiprocessing",
        "data plugin": "Builtin Parser",
        "Extras": args
    }
    return configuration