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
This file holds documentation...
"""

import os

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class AbstractSettingDocuments(object):

    def __init__(self, advanced = False):
        self.advanced = advanced

    @property
    def title(self):
        raise NotImplementedError


class DataSettingDocuments(AbstractSettingDocuments):

    _home = u""
    _title = {"name": u"Data Information", "default": u"", "required": True, "comment": u""}
    _qfactor = {"name": u"QFactor List Location", "default": _home + u"Qfactor.txt", "required": False,
                "comment": u"The file that holds the QFactor Data"}
    _save = {"name": u"Save Location", "default": _home + u"output.txt", "required": True,
             "comment": u"Where to save the data"}
    _accepted = {"name": u"Accepted Monte Carlo Location", "default": _home + u"accepted_data.csv", "required": False,
                 "comment": u"The file that holds the Accepted Monte Carlo data"}
    _data = {"name": u"Data Location", "default": _home + u"data.csv", "required": True,
             "comment": u"The file that holds the kinematic variable data"}
    _bin = {"name": u"Binned Location", "default": u"bins.txt", "required": False,
            "comment": u"The file that holds the binned data"}

    def __init__(self, accepted, bins, advanced):

        super(DataSettingDocuments, self).__init__(advanced)

        self.accepted = accepted
        self.bin = bins

        if os.name == "nt":
            self.home = u"C:/Users/user/My Documents/"
        elif os.name == "mac":
            self.home = u"/Users/user/Docs"
        else:
            self.home = u"/home/user/Documents/"



class MinuitSettingDocuments(AbstractSettingDocuments):
    title = {"name": u"Minuit's Settings", "default": u"", "required": True, "comment": u""}
    initial = {"name": u"Minuit's Initial Settings", "default": u"{ A1: 1, A2: 2}", "required": True, "comment": u""}
    parameters = {"name": u"Minuit's Parameters", "default": u"[A1, A2, A3]", "required": True, "comment": u""}
    strategy = {"name": u"Minuit's Strategy", "default": u"1", "required": False, "comment": u""}
    setup = {"name": u"Minuit's Set Up", "default": u"1", "required": False, "comment": u""}
    ncall = {"name": u"Minuit's ncall", "default": u"1000", "required": False, "comment": u""}

    def __init__(self, advanced):
        super(MinuitSettingDocuments, self).__init__(advanced)


class FunctionSettingDocuments(object):
    title = {"name": u"Function Settings", "default": u"", "required": True, "comment": u""}
    location = {"name": u"Function Location", "default": u"function.py", "required": True, "comment": u""}
    process = {"name": u"Processing Name", "default": u"the_function", "required": True, "comment": u""}
    setup = {"name": u"Setup Name", "default": u"the_setup", "required": True, "comment": u""}

    def __init__(self, advanced):
        super(FunctionSettingDocuments, self).__init__(advanced)


class GeneralSettingDocuments(object):
    title = {"name": u"General Settings", "default": u"", "required": True, "comment": u""}
    threads = {"name": u"Number of Threads", "default": u"auto", "required": True, "comment": u""}
    logging = {"name": u"Logging Level", "default": u"ERROR", "required": False, "comment": u""}

    def __init__(self, advanced):
        super(GeneralSettingDocuments, self).__init__(advanced)


class ExampleFunction(object):
    standard_function = u"""\
def the_function(the_array, the_params): #You can change both the variable names and function name
    the_size = len(the_array[list(the_array)[0]) #You can change the variable name here, or set the length of values by hand
    values = numpy.zeros(shape=the_size)
    for event in range(the_size):
        #Here is where you define your function.
        #Your array has to have a [event] after it so the for loop can iterate through all the events in the array
        values[event] = the_params["A1"] + the_array["kvar"][event] #Change "kvar" to the name of your vairable, and "A1" to your parameter
    return values
"""
    standard_setup = u"""\
def the_setup(): #This function can be renamed, but will not be sent any arguments.
    #This function will be ran once before the data is Minuit begins.
    pass
"""

    standard_import = u"import numpy"

