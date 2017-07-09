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
Arguments, for simple command line programs
-------------------------------------------
This module attempts to do a lot of the same functionality as the
Configurator, but instead of relying on a configuration file for the program
to run, it instead gets all its arguments from the command line.

This is best for programs and plugins that have very few potential options.

- _loader - this loads the plugins for the ArgumentParser
- arguments_options - A simple interface for Main Plugins.
- start - Main entry point for the Arg Parser, contains the chunk of code
  that parses the provided options into a simple program.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
