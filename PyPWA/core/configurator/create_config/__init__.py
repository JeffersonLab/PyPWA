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
Takes the initial information along with the various information from the 
user to dynamically create a template configuration file for the program 
they want to run using all the plugins they wish to use.

- _builder - Builds the configuration using all the information it can gather

- _input - Handles all user input into the program for the configuration

- create - The main entry point for the program.

.. todo::
    This entire module is actually in a rather bad state. The entire code 
    base has had careful thought behind its design, everything was written 
    with a clear purpose in mind.
    
    Not this module though, this module was written as a quick solution to 
    a complex problem. Now its in a awful state of rot, it's even been put 
    into its own folder so the smell doesn't carry far into the other 
    packages.
    
    What this package needs is a careful rebuilding using the same specs 
    that made this package, a new package that entirely replaces this 
    shameful waste of development resources.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
