"""
Entry point for console GeneralShell
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond", "Will Phelps", "Stephanie Bramlett"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import os
import sys
import argparse
import PyPWA.data.file_manager
import PyPWA.core.console_main


def start_console(desc):
    """Entry point for GeneralFitting"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("configuration", type=str, default="", nargs="?")
    parser.add_argument("--WriteConfig", "-wc", action="store_true", help="Write an example configuration to the current working directory" )
    parser.add_argument("--Version", "-V", action="version", version="%(prog)s (version 2.0.0b1)")
    args = parser.parse_args()
    if args.WriteConfig == False and args.configuration == '':
        parser.print_help()
    else:
        return args


def start_data(configuration):
    the_data = PyPWA.data.file_manager.MemoryInterface()
    the_config = the_data.parse(configuration)
    cwd = os.getcwd()
    sys.stderr.write("\x1b[2J\x1b[H")
    return [cwd, the_config]


def start_console_general_fitting():
    args = start_console("Fitting using the Maximum-Likelihood ")

    if args.WriteConfig:
        config = PyPWA.core.console_main.Configurations()
        with open(os.getcwd() + "/Example.yml", "w") as stream:
            stream.write(config.fitting_config())
        with open(os.getcwd() + "/Example.py", "w") as stream:
            stream.write(config.example_function())
    else:
        cwd, the_config = start_data(args.configuration)

        fitting = PyPWA.core.console_main.Fitting(the_config, cwd)
        fitting.start()


def start_console_general_simulator():
    """Entry point for GeneralSimulator"""
    parser = argparse.ArgumentParser(description="Simulation Using the Acceptance Rejection Method")
    parser.add_argument("configuration", type=str, default="", nargs="?")
    parser.add_argument("--WriteConfig", "-wc", action="store_true", help="Write an example configuration to the current working directory" )
    parser.add_argument("--Version", "-V", action="version", version="%(prog)s (version 2.0.0b1)")
    args = parser.parse_args()
    if args.WriteConfig is False and args.configuration == '':
        parser.print_help()
    else:
        if args.WriteConfig:
            config = PyPWA.core.console_main.Configurations()
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(config.simulator_config())
            with open(os.getcwd() + "/Example.py", "w") as stream:
                stream.write(config.example_function())
        else:
            the_data = PyPWA.data.file_manager.MemoryInterface()
            the_config = the_data.parse(args.configuration)
            cwd = os.getcwd()
            sys.stderr.write("\x1b[2J\x1b[H")

            simulating = PyPWA.core.console_main.Simulator(the_config, cwd)
            simulating.start()


def start_console_general_intensities():
    """Entry point for GenerateIntensities"""
    parser = argparse.ArgumentParser(description="Generate Intensities")
    parser.add_argument("configuration", type=str, default="", nargs="?")
    parser.add_argument("--WriteConfig", "-wc", action="store_true", help="Write an example configuration to the current working directory" )
    parser.add_argument("--Version", "-V", action="version", version="%(prog)s (version 2.0.0b1)")
    args = parser.parse_args()
    if args.WriteConfig is False and args.configuration == '':
        parser.print_help()
    else:
        if args.WriteConfig:
            config = PyPWA.core.console_main.Configurations()
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(config.intensities_config())
            with open(os.getcwd() + "/Example.py", "w") as stream:
                stream.write(config.example_function())
        else:
            the_data = PyPWA.data.file_manager.MemoryInterface()
            the_config = the_data.parse(args.configuration)
            cwd = os.getcwd()
            sys.stderr.write("\x1b[2J\x1b[H")

            simulating = PyPWA.core.console_main.Intensities(the_config, cwd)
            simulating.start()


def start_console_general_weighting():
    """Entry point for GenerateWeights"""
    parser = argparse.ArgumentParser(description="Generate Weights")
    parser.add_argument("configuration", type=str, default="", nargs="?")
    parser.add_argument("--WriteConfig", "-wc", action="store_true", help="Write an example configuration to the current working directory" )
    parser.add_argument("--Version", "-V", action="version", version="%(prog)s (version 2.0.0b1)")
    args = parser.parse_args()
    if args.WriteConfig is False and args.configuration == '':
        parser.print_help()
    else:
        if args.WriteConfig:
            config = PyPWA.core.console_main.Configurations()
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(config.simulator_config())
        else:
            the_data = PyPWA.data.file_manager.MemoryInterface()
            the_config = the_data.parse(args.configuration)
            cwd = os.getcwd()
            sys.stderr.write("\x1b[2J\x1b[H")

            simulating = PyPWA.core.console_main.Weights(the_config, cwd)
            simulating.start()


def start_console_general_chisquared():
    """Entry point for GenerateWeights"""
    parser = argparse.ArgumentParser(description="Generate Weights")
    parser.add_argument("configuration", type=str, default="", nargs="?")
    parser.add_argument("--WriteConfig", "-wc", action="store_true", help="Write an example configuration to the current working directory" )
    parser.add_argument("--Version", "-V", action="version", version="%(prog)s (version 2.0.0b1)")
    args = parser.parse_args()
    if args.WriteConfig is False and args.configuration == '':
        parser.print_help()
    else:
        if args.WriteConfig:
            config = PyPWA.core.console_main.Configurations()
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(config.chi_config())
        else:
            the_data = PyPWA.data.file_manager.MemoryInterface()
            the_config = the_data.parse(args.configuration)
            cwd = os.getcwd()
            sys.stderr.write("\x1b[2J\x1b[H")

            simulating = PyPWA.core.console_main.Chi(the_config, cwd)
            simulating.start()


# I hate this file
