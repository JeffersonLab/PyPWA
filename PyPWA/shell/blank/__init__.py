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

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.shell.blank import setup

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class BlankModule(options.Main):

    plugin_name = "blank shell module"
    setup = setup.BlankSetup
    required_plugins = [
        options.Types.DATA_PARSER
    ]

    default_options = {
        "Option 1": 1,
        "Option 2": "A string value",
        "Option 3": "Preset 1"
    }

    option_difficulties = {
        "Option 1": options.Levels.REQUIRED,
        "Option 2": options.Levels.OPTIONAL,
        "Option 3": options.Levels.ADVANCED
    }

    option_types = {
        "Option 1": int,
        "Option 2": str,
        "Option 3": ["Preset 1", "Preset 2", "Preset 3"]
    }

    module_comment = "BLANK MODULE"
    option_comments = {
        "Option 1": "If you see this in production something went wrong.",
        "Option 2": "If you see this in production something went wrong.",
        "Option 3": "If you see this in production something went wrong."
    }
