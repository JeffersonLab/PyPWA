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

from __future__ import absolute_import

import sys
import logging
import os

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

# Define the logger for the entire page since there are no objects here.
_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())


def import_object(file_location, object_name, cwd=False):
    """
    Takes a single file, imports it, then returns whatever the requested object
    was for the program or user to manipulate however they need.

    Args:
        file_location (str): The location to the file that needs to be imported.
        object_name (str): The name of the python object that needs to be
            imported.
        cwd (Optional[str]): The root directory of the file.

    Returns:
        The object that was called during the extraction process.

    Note:
        This file might support a list for the object_name in the future so that
        you can import multiple objects from the same file.
    """
    if not cwd:
        _LOGGER.debug("Common Working Directory not found, using path from the "
                      "provided file location.")
        cwd = _cwd_from_path(file_location)

    # Here I take the cwd that was either found or provided, then I append that
    # base directory to Python's path. After that I import the entire file
    # into a variable so that I can extract the needed object out into its own
    # variable that will be returned to the calling method.
    sys.path.append(cwd)
    imported = __import__(os.path.basename(file_location).strip(".py"))
    loaded_object = getattr(imported, object_name)
    return loaded_object


def _cwd_from_path(file_location):
    """
    This internal function specifically extracts the common working directory
    of the file that needs to be loaded from the path of the file. It does it
    by finding the absolute path of the file, then striping the file from the
    path.

    Args:
        file_location (str): The path to the file.

    Returns:
        str: The full path to the folder including the file.
    """
    return os.path.dirname(os.path.abspath(file_location))

