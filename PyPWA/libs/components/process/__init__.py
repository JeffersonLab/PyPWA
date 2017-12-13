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
This is the builtin plugin for Multiprocessing, it works by taking the
users kernels and interface and nesting them into their own individual
processes and the interface that is connected to them, then returns that
interface so that the user can manipulate those processes.

Example:
    foreman = CalculationForeman()
    foreman.populate(AbstractInterface, AbstractKernels)
    interface = foreman.fetch_interface()
    processed_value = interface.run("Your args")
"""

import multiprocessing

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator import options
from PyPWA.libs.components.process import foreman

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Processing(options.Component):

    def __init__(self):
        self.name = "Multiprocessing"
        self.module_comment = "OpenMP like Python Implementation"

    def get_default_options(self):
        return {
            "number of processes": multiprocessing.cpu_count() * 2
        }

    def get_option_difficulties(self):
        return {
            "number of processes": options.Levels.OPTIONAL
        }

    def get_option_types(self):
        return {
            "number of processes": int
        }

    def get_option_comments(self):
        return {
            "number of processes": "Number of processes to use for "
                                   "calculation."
        }
