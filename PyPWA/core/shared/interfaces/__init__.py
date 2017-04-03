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
The universal interfaces for all of PyPWA.
------------------------------------------
These interfaces define how the objects should interact with each other in 
all circumstances inside PyPWA. These interfaces however do not define how 
the plugins should interact with the initializer. 

.. note::
    Information and the needed interfaces to interact with an 
    initializer should be stated inside the respective initializer.

- internals - This contains how the internal objects and information passed 
  around by the main objects should be defined.
  
- plugins - This contains information on the methods that are expected to 
  exist inside the plugin objects.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
