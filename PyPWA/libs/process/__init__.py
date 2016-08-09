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

from PyPWA.configurator import templates
from PyPWA.libs.process import kernels
from PyPWA.libs.process import foreman
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Processing(templates.TemplateOptions):

    def _plugin_name(self):
        return kernels.MODULE_NAME

    def _plugin_interface(self):
        return foreman.CalculationForeman

    def _plugin_type(self):
        return self._kernel_processing

    def _plugin_requires(self):
        return False

    def _plugin_arguments(self):
        return {
            "interface": kernels.AbstractInterface,
            "process": kernels.AbstractKernel
        }

    def _default_options(self):
        return {
            "number of processes": multiprocessing.cpu_count() * 2
        }

    def _option_levels(self):
        return {
            "number of processes": self._optional
        }

    def _option_types(self):
        return {
            "number of processes": int
        }

    def _main_comment(self):
        return "This is the builtin processing plugin, you can replace " \
               "this with your own, or use one of the other options " \
               "that we have."

    def _option_comments(self):
        return {
            "number of processes":
                "This is the max number of processes to have running at "
                "any time in the program, the hard max will always be 2 "
                "* the number of CPUs in your computer so that we don't "
                "resource lock your computer. Will work on any Intel  or "
                "AMD processor, PowerPCs might have difficulty here."
        }
