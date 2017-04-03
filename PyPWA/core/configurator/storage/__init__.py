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
For directly interacting with plugins and mains
-----------------------------------------------
This package was written to store the plugins and important information 
regarding the plugins.

- core_storage - Core plugin storage. Has objects that store the plugins 
  and mains separately, and lets you extract plugins via name or type.
  
- module_fetcher - lets you specify main or plugin by their name.

- template_parser - Parses all the plugins templates together to create one
  large template dictionary.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
