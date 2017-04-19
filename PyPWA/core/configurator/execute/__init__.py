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
Where the program starts.
-------------------------
This module takes the written configuration file along with some information
from the entry point and tries to use that attempt to load the plugins and 
start the program.

- _correct_configuration - Corrects the parsed configuration file using the
  rendered template dict from all the known plugins.
  
- _plugin_data - Contains the logic pertaining to loading the plugins listed
  in the user's config file and initializing it with the users settings
  
- _settings - Reads in the configuration file, processes the overrides, 
  appends the plugin directory to the plugin search path, then corrects the
  received values using _correct_configuration.
  
- _storage_data - contains the objects that operate directly with the loaded
  plugins.

- start - Where the main source of execution occurs for the program.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
