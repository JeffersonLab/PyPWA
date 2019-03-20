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

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

from .factory import make_processes
from .templates import Interface, Kernel
from ._processes import ProcessCodes
