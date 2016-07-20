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

import ruamel.yaml.comments

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


class Options(object):
    _options = {

        # Optional
        "number of processes": multiprocessing.cpu_count() * 2
        #  We set this two 2 times the number of CPUs to account for
        #  hyper threading.
    }

    _template = {
        "number of processes": int
    }

    def __init__(self):
        """
        Simple Object to hold the options for the Foreman.
        """
        header = self._build_empty_options_with_comments()
        self._optional = self._build_optional(header)
        self._required = header

    @staticmethod
    def _build_empty_options_with_comments():
        header = ruamel.yaml.comments.CommentedMap()
        content = ruamel.yaml.comments.CommentedMap()

        header[kernels.MODULE_NAME] = content
        header.yaml_add_eol_comment(
            "This is the builtin processing plugin, you can replace this "
            "with your own, or use one of the other options that we have."
            , kernels.MODULE_NAME
        )

        content.yaml_add_eol_comment(
            "This is the max number of processes to have running at any "
            "time in the program, the hard max will always be 2 * the "
            "number of CPUs in your computer so that we don't resource "
            "lock your computer. Will work on any Intel  or AMD "
            "processor, PowerPCs might have difficulty here.",
            "number of processes"
        )

        return header

    def _build_optional(self, header):
        """
        Since there is only one option, and its optional, we only have a
        single building function for the actual options.

        Args:
            header (ruamel.yaml.comments.CommentedMap): The empty
                dictionary with the comments included.

        Returns:
            ruamel.yaml.comments.CommentedMap: The dictionary with the
                optional fields.
        """
        header[kernels.MODULE_NAME]["number of processes"] = \
            self._options["number of processes"]
        return header

    @property
    def return_template(self):
        return self._template

    @property
    def return_required(self):
        return self._required

    @property
    def return_optional(self):
        return self._optional

    @property
    def return_advanced(self):
        return self._optional

    @property
    def return_defaults(self):
        return self._options

metadata = [{
    "name": kernels.MODULE_NAME,
    "provides": "kernel processing",
    "interface": foreman.CalculationForeman,
    "arguments": {
        "interface": kernels.AbstractInterface,
        "process": kernels.AbstractKernel
    },
    "requires function": False
}]
