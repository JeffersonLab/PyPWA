"""
Entry point for console GeneralShell
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"
import argparse


class ConsoleArgumentParsing(object):

    def __init__(self, the_description):
        parser = argparse.ArgumentParser(description=the_description)
        parser.add_argument("configuration", type=str, default="", nargs="?")
        parser.add_argument("--WriteConfig", "-wc", action="store_true", help="Write an example configuration to the "
                            "current working directory")
        parser.add_argument("--Version", "-V", action="version", version="%(prog)s (version " + __version__ +
                            __status__ + ")")
        self._args = parser.parse_args()
        if not self._check_arguments(self._args):
            parser.print_help()
            exit()

    @staticmethod
    def _check_arguments(arg):
        if arg.WriteConfig is False and arg.configuration == "":
            return False
        else:
            return True

    @property
    def config_location(self):
        return self._args.configuration

    @property
    def write_config(self):
        return self._args.WriteConfig
