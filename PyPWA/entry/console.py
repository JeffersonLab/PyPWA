#!/usr/bin/env python

"""
console.py: Entry point for the General Shell
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "[CURRENT_VERSION]"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "[CURRENT_STATUS]"

import  click, PyPWA.data.filehandler, os, PyPWA.core.console

@click.command()
@click.argument( "configuration", nargs=-1, type=click.Path(exists=True))
@click.option("--WriteConfig", "-wc", multiple=True, default=False, help="Write an example configuration to the current working directory", is_flag=True)
@click.version_option()
def start_console_general_fitting(configuration, writeconfig):
    """
    Parses <configuration> for settings and then uses them to the General Fitting utility.
    """
    if len(configuration) == 0 and len(writeconfig) == 0:
        click.secho("Use \"GeneralFitting --help\" for the proper way to use the utility", bold=True)
    else:
        if writeconfig:
            config = PyPWA.core.console.Configurations()
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(config.fitting_config)
            with open(os.getcwd() + "/Example.py", "w") as stream:
                stream.write(config.example_function)
        else:
            the_data = PyPWA.data.filehandler.MemoryInterface()
            the_config = the_data.parse(configuration[0])
            cwd = os.getcwd()
            click.clear()
            
            fitting = PyPWA.core.console.Fitting(the_config, cwd)
            fitting.start()

@click.command()
@click.argument( "configuration", nargs=-1, type=click.Path(exists=True))
@click.option("--WriteConfig", "-wc", multiple=True, default=False, help="Write an example configuration to the current working directory", is_flag=True)
@click.version_option()
def start_console_general_simulator(configuration, writeconfig):
    """
    Parses <configuration> for settings and then uses them to the General Simulator utility.
    """
    if len(configuration) == 0 and len(writeconfig) == 0:
        click.secho("Use \"GeneralSimulator --help\" for the proper way to use the utility", bold=True)
    else:
        if writeconfig:
            config = PyPWA.core.console.Configurations()
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(config.simulator_config)
            with open(os.getcwd() + "/Example.py", "w") as stream:
                stream.write(config.example_function)
        else:
            the_data = PyPWA.data.Interface()
            the_config = the_data.parse(configuration[0])
            cwd = os.getcwd()
            click.clear()
            
            simulating = PyPWA.core.console.Simulator(the_config, cwd)
            simulating.start()