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
The core libraries of PyPWA
---------------------------
Any core libraries that are needed for PyPWA that wouldn't or shouldn't 
function as a plugin, are located here. This means anything whose internal 
function shouldn't really change should be here, such as hash generation, 
data location, and such.

- interfaces - The interfaces to the program, while the configurator and 
  other initializing packages may offer their own interfaces to load into 
  the program. These interfaces actually define how the objects should 
  interact with each other instead.
   
- files - A package containing a collection of modules whose focus is handling
  file data for the package. This includes hashing, locations, and file
  length.
  
- initial_logging - Controls how logging works in PyPWA. Currently is 
  limited to string logging.
  
- plugin_loader - The main plugin loading module inside PyPWA. It's generic 
  enough to be used anywhere but also powerful enough to handle all plugin 
  needs.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
