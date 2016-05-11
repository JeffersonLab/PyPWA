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
PyPWA is an attempt to have a set multiprocessing tools to easy the Partial Wave
Analysis process.

Current there is a multiprocessing tool for both the Acceptance Rejection Model,
and the Maximum-Likelihood Estimation for fitting.

The tools work with Kinematic Variables defined in standard text files, Comma
Separated Variables, and Tab Seperated Variables.

Example:
    For both the GeneralFitting and the GeneralSimulator you should
    first run [tool] -wc, ie:
        $ GeneralFitting -wc
    then afterwords modify and rename the Example.yml and Example.py
    files that are generated.
    Lastly to actually run the tool with your freshly created
    configuration file, run [tool] <configuration>.yml, ie:
        $ GeneralFitting Example.yml
"""

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__email__ = "maj@jlab.org"
__status__ = "development"
__maintainer__ = ["Mark Jones"]
__version__ = "2.0.0b2"

VERSION = __version__
STATUS = __status__
LICENSE = __license__
