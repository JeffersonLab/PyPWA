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
Where everything begins.
------------------------
This is the starting objects for the configurator. This handles initial 
output, argument parsing, logging, and the finally depending on the 
arguments will start building the configuration, or it will execute the 
program.

- _Arguments - A simple object that parses the arguments for the program, 
  then exposes those inputs through the properties.
  
- StartProgram - This is the object that takes the information from the 
  entry point along with the data from the _Arguments to determine where 
  which half of the configuration utility should be started. 
"""

import argparse
import logging
import sys
from typing import Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator.create_config import create
from PyPWA.core.configurator.execute import start
from PyPWA.core.shared import initial_logging

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _Arguments(object):

    def __init__(self):
        self.__parser = None  # type: argparse.ArgumentParser
        self.__arguments = None  # type: argparse.Namespace()

    def parse_arguments(self, description):
        # type: (str) -> None
        self.__set_arguments(description)
        self.__parse_arguments()
        self.__quit_if_no_args()

    def __set_arguments(self, description):
        # type: (str) -> None
        self.__set_parser(description)
        self.__add_configurator_argument()
        self.__add_write_config_argument()
        self.__add_verbose_argument()
        self.__add_log_file_argument()
        self.__add_version_argument()

    def __set_parser(self, description):
        # type: (str) -> None
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

    def __add_verbose_argument(self):
        self.__parser.add_argument(
            "-v", action="count", default=0,
            help="Adds logging, defaults to errors, then setups up on "
                 "from there. -v will include warning, -vv will show "
                 "warnings and info, and -vvv will show info, warnings, "
                 "debugging."
        )

    def __add_log_file_argument(self):
        self.__parser.add_argument(
            "--log-file", "-l", type=str, default="", nargs="?"
        )

    def __add_version_argument(self):
        self.__parser.add_argument(
            "--Version", "-V", action="version",
            version="%(prog)s (version " + __version__ + ")"
        )

    def __parse_arguments(self):
        self.__arguments = self.__parser.parse_args()

    def __quit_if_no_args(self):
        if not self.write_config and self.configuration_location == "":
            self.__parser.print_help()
            sys.exit()

    @property
    def write_config(self):
        # type: () -> bool
        return self.__arguments.WriteConfig

    @property
    def configuration_location(self):
        # type: () -> str
        return self.__arguments.configuration

    @property
    def verbose(self):
        # type: () -> int
        return self.__arguments.v

    @property
    def log_file(self):
        # type: () -> str
        return self.__arguments.log_file


class StartProgram(object):

    def __init__(self):
        self.__execute = start.Execute()
        self.__create_config = create.StartConfig()
        self.__arguments = _Arguments()
        self.__configuration = None  # type: dict

    def start(self, configuration):
        # type: (Dict[str, str]) -> None
        self.__set_configuration(configuration)
        self.__process_extras()
        self.__load_arguments()
        self.__begin_output()
        self.__setup_logger()
        self.__process_arguments()

    def __set_configuration(self, configuration):
        # type: (Dict[str, str]) -> None
        self.__configuration = configuration

    def __process_extras(self):
        if self.__configuration["extras"]:
            print(
                "[ERROR] Caught something unaccounted for, "
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
        # type: () -> str
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

Built in Jefferson Lab.
"""

    def __setup_logger(self):
        if self.__arguments.verbose == 1:
            initial_logging.InternalLogger.configure_root_logger(
                logging.WARNING, self.__arguments.log_file
            )
        elif self.__arguments.verbose == 2:
            initial_logging.InternalLogger.configure_root_logger(
                logging.INFO, self.__arguments.log_file
            )
        elif self.__arguments.verbose >= 3:
            initial_logging.InternalLogger.configure_root_logger(
                logging.DEBUG, self.__arguments.log_file
            )
        else:
            initial_logging.InternalLogger.configure_root_logger(
                logging.ERROR, self.__arguments.log_file
            )

    def __process_arguments(self):
        if self.__arguments.write_config:
            self.__write_config()
        else:
            self.__run_builder()

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
