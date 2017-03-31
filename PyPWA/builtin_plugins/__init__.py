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
All the plugins that come packaged with PyPWA by default.
---------------------------------------------------------

- data - A not so basic data plugin that supports caching, different file 
  types, can be extended, and even supports both parsing and iterating.

- minuit - A python / cython minimizer based on ROOT's PyPWA.

- nestle - A python maximizer based off of Multinest.

- process - A Kernel based multiprocessing module. Allows for an 
  embarrassingly parallel calculation to be expanded across multiple cores.
  
For more information about how these plugins work, see their documentation 
as well.
"""


from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
