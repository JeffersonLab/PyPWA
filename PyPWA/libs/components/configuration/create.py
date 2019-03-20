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

"""

import enum
import json
import yaml
from typing import Any, Dict, List

from PyPWA import AUTHOR, VERSION, Path

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Verbosity(enum.Enum):
    REQUIRED = 0
    OPTIONAL = 1
    ALL = 2


def make_configuration(
        configuration_location, default_options,
        option_verbosity, selected_verboseness
):
    # type: (Path, Dict[str, Any], Dict[str, Any], Verbosity) -> None
    processed_configuration = _ConfigVerbosity.process(
        default_options, option_verbosity, selected_verboseness
    )
    _write_configuration(configuration_location, processed_configuration)


class _ConfigVerbosity(object):

    @classmethod
    def process(cls, default_options, option_verbosity, verboseness):
        # type: (Dict[str, Any], Dict[str, Any], Verbosity) -> Dict[str, Any]
        if verboseness == Verbosity.ALL:
            return default_options
        else:
            keep_list = cls.__get_keep_list(verboseness)
            return cls.__remove_unneeded_options(
                default_options, option_verbosity, keep_list
            )

    @staticmethod
    def __get_keep_list(verboseness):
        # type: (Verbosity) -> List[Verbosity]
        if verboseness == Verbosity.REQUIRED:
            return [Verbosity.REQUIRED]
        elif verboseness == Verbosity.OPTIONAL:
            return [Verbosity.REQUIRED, Verbosity.OPTIONAL]
        else:
            raise ValueError("Unknown value {0}!".format(verboseness))

    @classmethod
    def __remove_unneeded_options(
            cls,
            defaults,  # type: Dict[str, Any]
            option_verbosity,  # type: Dict[str, Any]
            keep_list  # type: List[Verbosity]
    ):
        # type: (...) -> Dict[str, Any]
        processed_configuration = dict()
        for option, verbosity in option_verbosity.items():
            if isinstance(verbosity, dict):
                child = cls.__remove_unneeded_options(
                    defaults[option], option_verbosity[option], keep_list
                )
                if len(child.items()):
                    processed_configuration[option] = child
            elif verbosity in keep_list:
                processed_configuration[option] = defaults[option]
        return processed_configuration


def _write_configuration(conf_location, processed_configuration):
    # type: (Path, Dict[str, Any]) -> None
    with conf_location.open('w') as stream:
        if conf_location.suffix == ".json":
            json.dump(stream, processed_configuration, indent=4)
        else:
            stream.write(yaml.dump(processed_configuration))
