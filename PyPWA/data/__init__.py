"""
PyPWA.lib.data:
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "[CURRENT_VERSION]"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "[CURRENT_STATUS]"

class Interface(object)

    supported_file_types = { "Kv": ".txt" }

    cache = True

    files_to_load = {}

    def __init__(self, config = None):
        if config != None:
            self.cache = config["Use Cache"]
            self.files_to_load = 