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
Creates the initial configuration template for users to modify.
---------------------------------------------------------------

- _builder - Builds the actual configuration for the program.

- _input_loop - Provides a simple object to extend for defining questions.

- _level_processing - takes a plugin and a requested level and returns
  the needed options for the selected difficulty.
  
- _metadata - Objects that interact directly with the plugins and shells,
  determines which plugins to load.

- _override - Overrides options and keys in the created 
  template configuration.
  
- _questions - Stores questions that the user can be asked.

- _writer - Each of the potential configuration writers are defined here.

- create - The main object for create_config.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
