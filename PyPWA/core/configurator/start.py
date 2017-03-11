#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This file is the main file for all of PyPWA. This file takes a
configuration file, processes it, then contacts the main module that is
requested to determine what information is needed to be loaded and how it
needs to be structured to be able to function in the users desired way.
"""

import argparse
import logging
import sys

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.shared import initial_logging
from PyPWA.core.configurator.create_config import create
from PyPWA.core.configurator.execute import start

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _Arguments(object):

    __parser = None  # type: argparse.ArgumentParser()
    __arguments = None  # type: argparse.Namespace()

    def parse_arguments(self, description):
        self.__set_arguments(description)
        self.__parse_arguments()
        self.__quit_if_no_args()

    def __set_arguments(self, description):
        self.__set_parser(description)
        self.__add_configurator_argument()
        self.__add_verbose_argument()
        self.__add_version_argument()
        self.__add_write_config_argument()

    def __set_parser(self, description):
        self.__parser = argparse.ArgumentParser(description=description)

    def __add_configurator_argument(self):
        self.__parser.add_argument(
            "configuration", type=str, default="", nargs="?"
        )

    def __add_write_config_argument(self):
        self.__parser.add_argument(
            "--WriteConfig", "-wc", action="store_true",
            help="Write an example configuration to the current working "
                 "directory"
        )

    def __add_version_argument(self):
        self.__parser.add_argument(
            "--Version", "-V", action="version",
            version="%(prog)s (version " + __version__ + ")"
        )

    def __add_verbose_argument(self):
        self.__parser.add_argument(
            "--verbose", "-v", action="count",
            help="Adds logging, defaults to errors, then setups up on "
                 "from there. -v will include warning, -vv will show "
                 "warnings and info, and -vvv will show info, warnings, "
                 "debugging."
        )

    def __parse_arguments(self):
        self.__arguments = self.__parser.parse_args()

    def __quit_if_no_args(self):
        if not self.write_config and self.configuration_location == "":
            self.__parser.print_help()
            sys.exit()

    @property
    def write_config(self):
        return self.__arguments.WriteConfig

    @property
    def configuration_location(self):
        return self.__arguments.configuration_location

    @property
    def verbose(self):
        return self.__arguments.verbose


class StartProgram(object):

    __configuration = None  # type: dict

    __execute = start.SetupSettings()
    __create_config = create.Config()
    __arguments = _Arguments()

    def start(self, configuration):
        self.__set_configuration(configuration)
        self.__process_extras()
        self.__load_arguments()
        self.__begin_output()
        self.__set_logging_level()
        self.__process_arguments()

    def __set_configuration(self, configuration):
        self.__configuration = configuration

    def __process_extras(self):
        if self.__configuration["extras"]:
            print(
                "[INFO] Caught something unaccounted for, "
                "this should be reported, caught: "
                "{}".format(self.__configuration["extras"][0])
            )

    def __load_arguments(self):
        self.__arguments.parse_arguments(self.__configuration["description"])

    def __begin_output(self):
        sys.stdout.write("\x1b[2J\x1b[H")  # Clears the screen
        sys.stdout.write(self.__opening_art())

    @staticmethod
    def __opening_art():
        return """\
#########          ######### ##                ##  ###
##      ##         ##      ## ##              ##  ## ##
##      ##         ##      ##  ##            ##  ##   ##
#########          #########    ##    ##    ##  ##     ##
##       ##     ## ##            ##  ####  ##  ## ##### ##
##        ##   ##  ##             ####  ####  ##         ##
##         ## ##   ##              ##    ##  ##           ##
            ##
           ##                      $$$$$$$$  $   $   $$$$$ $$      $$
         ###                      $$$       $$   $$ $      $$      $$
                                   $$$$$$$  $$$$$$$ $$$$$$ $$      $$
                                        $$$ $$   $$ $      $$      $$
                                  $$$$$$$$   $   $   $$$$$  $$$$$$  $$$$$$

Developed By:
    Mark Jones: maj@jlab.org

Credit:
    Dr. Carlos Salgado: salgado@jlab.org
    Will Phelps: wphelps@jlab.org
    Joshua Pond
"""

    def __set_logging_level(self):
        if self.__arguments.verbose == 1:
            initial_logging.define_logger(logging.WARNING)
        elif self.__arguments.verbose == 2:
            initial_logging.define_logger(logging.INFO)
        elif self.__arguments.verbose >= 3:
            initial_logging.define_logger(logging.DEBUG)
        else:
            initial_logging.define_logger(logging.ERROR)

    def __process_arguments(self):
        if self.__arguments.configuration_location == "":
            self.__run_builder()
        else:
            self.__write_config()

    def __run_builder(self):
        self.__execute.run(
            self.__configuration,
            self.__arguments.configuration_location
        )

    def __write_config(self):
        self.__create_config.make_config(
            self.__configuration,
            self.__arguments.configuration_location
        )

