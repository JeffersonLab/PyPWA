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

import  click, PyPWA.data, PyPWA.proc, PyPWA.config, os

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
        import PyPWA.core.console
        fit = PyPWA.core.console.Fitting()
        if writeconfig:
            with open(os.getcwd() + "/Example.yml", "w") as stream:
                stream.write(fit.example_config)
            with open(os.getcwd() + "/Example.py", "w") as stream:
                stream.write(fit.example_function)
        else:
            the_configure = PyPWA.config.YAML()
            config = the_configure.generate(configuration[0])
            config["General Settings"]["cwd"] = os.getcwd()
            click.clear()
            fit.config = config
            fit.start()
