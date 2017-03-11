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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator import options
from PyPWA.builtin_plugins.process import foreman

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Processing(options.Plugin):

    plugin_name = "Builtin Multiprocessing"
    setup = options.Setup
    provides = options.Types.KERNEL_PROCESSING
    defined_function = None
    module_comment = "Builtin SMP Plugin, should be 'good enough'"

    default_options = {
        "number of processes": multiprocessing.cpu_count() * 2
    }

    option_levels = {
        "number of processes": options.Levels.OPTIONAL
    }

    option_types = {
        "number of processes": int
    }

    option_comments = {
        "number of processes": "Number of processes to use for calculation."
    }
