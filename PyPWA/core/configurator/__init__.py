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
A Yml based configuration initializer for PyPWA.
------------------------------------------------
This initializer takes a configuration file and uses it to initialize the 
requested objects, to start the program. It also can take all the available 
plugins and render those into a template configuration file.

- create_config - That package that contains all the code needed to create 
  a configuration file from the available plugins, also contains the logic 
  for the questions and input handled for the --WriteConfig

- execute - This takes a already made configuration file and then renders 
  it into requested objects that then becomes the program.
  
- storage - Here are where the loading and parsing of options from the 
  plugins is done. Each of these work with **all** plugins.
  
- option_tools - the various little objects needed to parse and pass 
  information between the plugins.
  
- options - The interfaces needed to create a plugin that can interact with 
  the configurator.
  
- start - Argument loading, logging, and initial setup for the configurator.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ConfiguratorOptions(options.Plugin):

    plugin_name = "Global Options"
    default_options = {
            "plugin directory": "none",
            "logging": "error"
        }

    option_difficulties = {
            "plugin directory": options.Levels.ADVANCED,
            "logging": options.Levels.OPTIONAL
        }

    option_types = {
            "plugin directory": str,
            "logging": [
                "debug", "info", "warning",
                "error", "critical", "fatal"
            ]
        }

    option_comments = {
            "plugin directory": "Directory for any plugins you may have.",
            "logging": "How much logging to enable, overridden by -v"
    }

    module_comment = "These settings effect runtime settings for the program."
