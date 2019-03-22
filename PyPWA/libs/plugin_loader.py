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

import importlib
import logging
import pkgutil
from typing import Any, List

from PyPWA import AUTHOR, VERSION
from .file.processor import templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


_LOGGER = logging.getLogger(__name__)


def fetch_plugins(root: type(templates), plugin_type: str) -> List[Any]:
    plugins = []
    plugin_path, plugin_name = (root.__path__, root.__name__ + ".")

    for f, name, i in pkgutil.iter_modules(plugin_path, plugin_name):
        plugins.append(_import_plugin(name, plugin_type))
        _LOGGER.debug("Loaded Data Plugin: {0}".format(name))

    return [plugin for plugin in plugins if plugin]  # Remove Nones


def _import_plugin(name: str, plugin_type: str) -> List[type(templates)]:
    try:
        return importlib.import_module(name).metadata
    except ImportError as error:
        _LOGGER.exception(error)
    except AttributeError as error:
        _LOGGER.error(
            "{0} plugin {1} has no metadata object! {2}".format(
                plugin_type, name, error
            )
        )
