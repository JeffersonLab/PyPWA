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
All the generic builtin plugins that come prepackaged with PyPWA are in this
portion of the module.

Here we have one data plugin, one processing module, and two optimizers:
    builtin_plugins.data is for data.
    builtin_plugins.process is a kernel based multiprocessing module.
    builtin_plugins.minuit is an optimizer that minimizes functions.
    builtin_plugins.nestle is an optimizer that maximizes functions.
    
Look at the documentation for each module for information about how the
module works or how to utilize the module.
"""


from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
