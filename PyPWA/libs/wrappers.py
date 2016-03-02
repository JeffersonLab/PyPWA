"""
Entry point for console GeneralShell
"""
import argparse
import os
import sys
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


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
                self.write_config(application_configuration["Configuration"], application_configuration["Python File"])

            sys.stdout.write("\x1b[2J\x1b[H")

            self.builder.run(application_configuration["Calculation"], arguments.configuration)

        return decorated_builder()

    @staticmethod
    def parse_arguments(application_configuration):
        parser = argparse.ArgumentParser(description=application_configuration["Description"])
        parser.add_argument("configuration", type=str, default="", nargs="?")
        parser.add_argument("--WriteConfig", "-wc", action="store_true",
                            help="Write an example configuration to the current working directory")
        parser.add_argument("--Version", "-V", action="version",
                            version="%(prog)s (version " + __version__ + " " + __status__ + ")")
        if application_configuration["AdvancedHelp"]:
            parser.add_argument("--AdvancedHelp", "-ah", action="store_true",
                                help="Prints the in depth advanced help to the terminal")

        arguments = parser.parse_args()

        if application_configuration["AdvancedHelp"] and arguments.AdvancedHelp:
            raise NotImplementedError("Currently advanced help output is undeveloped")

        if not arguments.WriteConfig and arguments.configuration == "":
            parser.print_help()

        return arguments

    @staticmethod
    def write_config(configuration, python, cwd=os.getcwd()):
        with open(cwd + "/Example.yml", "w") as stream:
            stream.write(configuration)
        with open(cwd + "/Example.py", "w") as stream:
            stream.write(python)
