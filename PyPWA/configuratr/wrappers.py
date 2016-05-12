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
This file is the main file for all of PyPWA. This file takes a
configuration file, processes it, then contacts the main module that is
requested to determine what information is needed to be loaded and how it needs
to be structured to be able to function in the users desired way.
"""

import argparse
import os
import sys

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class StartBuilder(object):
    def __init__(self, builder, *args):
        self.builder = builder(args)

    def __call__(self, function):
        def decorated_builder(*args):
            application_configuration = function(args)
            if application_configuration["Extras"]:
                return
            arguments = self.parse_arguments(application_configuration)

            if arguments.WriteConfig:
                self.write_config(application_configuration["Configuration"],
                                  application_configuration["Python File"])

            sys.stdout.write("\x1b[2J\x1b[H")

            self.builder.run(application_configuration["Calculation"],
                             arguments.configuration)

        return decorated_builder()

    @staticmethod
    def parse_arguments(app_config):
        parser = argparse.ArgumentParser(description=app_config["Description"])
        parser.add_argument("configuration", type=str, default="", nargs="?")
        parser.add_argument("--WriteConfig", "-wc", action="store_true",
                            help="Write an example configuration to the current"
                                 " working directory")

        parser.add_argument("--Version", "-V", action="version",
                            version="%(prog)s (version " + __version__ + ")")
        if app_config["AdvancedHelp"]:
            parser.add_argument("--AdvancedHelp", "-ah", action="store_true",
                                help="Prints the in depth advanced help to "
                                     "the terminal")

        arguments = parser.parse_args()

        if app_config["AdvancedHelp"] and arguments.AdvancedHelp:
            raise NotImplementedError("Currently advanced help output is "
                                      "undeveloped")

        if not arguments.WriteConfig and arguments.configuration == "":
            parser.print_help()

        return arguments

    @staticmethod
    def write_config(configuration, python, cwd=os.getcwd()):
        with open(cwd + "/Example.yml", "w") as stream:
            stream.write(configuration)
        with open(cwd + "/Example.py", "w") as stream:
            stream.write(python)
