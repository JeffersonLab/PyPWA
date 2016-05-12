# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This file imports the uses python files and plugins from their specified
location. This is an internal file only, and should be only be used by the
configuratr.
"""

import sys
import logging
import warnings

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class FunctionLoading(object):
    def __init__(self, cwd, function_location, function_name, setup_name):
        """
        This object loads the users python files into the program to be
        executed. I can not stress enough to verify the code before you import
        it, and do not import random python files you found online. Files with
        malicious intent can easily do permanent damage to your machine and
        your data. Use unverified code at your own risk!

        Args:
            cwd (str): The root directory where the files are held.
            function_location (str): The path to the python file.
            function_name (str): The name of the function that you want to load.
            setup_name (str): The name of the function you want to call before
                you execute your main function.
        """
        self._logger = logging.getLogger(__name__)
        self._users_amplitude, self._users_setup = self._import_function(
            cwd, function_location, function_name, setup_name
        )

    @staticmethod
    def _import_function(cwd, function_location, function_name, setup_name):
        """
        Imports and sets up functions for usage.

        Args:
            cwd (str): Path to folder with the functions
            function_location (str): Path to the file
            function_name (str): Name of Amplitude function
            setup_name (str): Name of Setup function.

        Returns:
            list: [ amplitude function, setup function ]
        """
        sys.path.append(cwd)
        try:
            imported = __import__(function_location.strip(".py"))
        except ImportError:
            raise

        try:
            users_amplitude = getattr(imported, function_name)
        except:
            raise

        try:
            setup_function = getattr(imported, setup_name)
        except AttributeError:
            warnings.warn(("Setup function  {0} was not found in {1},"
                           "going without setup function").format(setup_name, function_location), UserWarning)

            def empty():
                pass
            setup_function = empty

        return [users_amplitude, setup_function]

    @property
    def return_amplitude(self):
        return self._users_amplitude

    @property
    def return_setup(self):
        return self._users_setup
