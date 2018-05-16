#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import setuptools

__author__ = "PyPWA Team and Contributors"
__license__ = "GPLv3"
__version__ = "2.3.0.dev"
__email__ = "pypwa@jlab.org"
__status__ = "development"


configurator_entry = "PyPWA.entries.configurator"
argument_entry = "PyPWA.entries.arguments"

entry_points = {
    "console_scripts": [
        "PyFit = %s:py_fit" % configurator_entry,
        "LikelihoodFit = %s:likelihood_fit" % configurator_entry,
        "ChiSquaredFit = %s:chi_squared_fit" % configurator_entry,
        "PySimulate = %s:py_simulate" % configurator_entry,
        "GenerateIntensities = %s:generate_intensities" % configurator_entry,
        "GenerateWeights = %s:generate_weights" % configurator_entry,
        "PyMask = %s:masking_utility" % argument_entry
    ]
}

requires = [
    "tqdm",          # Progress Bars
    "iminuit<2.0",   # Default minimizer
    "scipy",         # Needed for Nestle with multiple ellipsoids.
    "nestle",        # New more advanced minimizer
    "numpy>1,<2.0",  # Arrays and optimizations
    "ruamel.yaml<0.15",   # Advanced YAML Parser
    "tabulate",      # Great aesthetic tables
    "appdirs",       # Attempts to find data locations
    "fuzzywuzzy",    # Fuzzes the user input
    "python-Levenshtein"
]

extras = dict()

tests = [
    'pytest',
    'pytest-runner',
    "pytest-cov",
    "pytest-logging"
]

# Handle differences in setuptools versions.
python_version = sys.version_info[0:2]
setuptools_version = int(setuptools.__version__.split(".", 1)[0])

if setuptools_version > 20:
    requires.append("enum34;python_version<'3.4'")
    requires.append("pathlib2;python_version<'3.5'")
    requires.append("typing;python_version<'3.5'")
elif 18 < setuptools_version < 20:
    extras[':python_version<"3.4"'] = ["enum34"]
    extras[':python_version<"3.5"'] = ["typing", "pathlib2"]
else:
    if "bdist_wheel" in sys.argv:
        # We want to raise an error here, wheels are universal, but
        # if extra packages aren't passed with a python version number
        # it will cause issues if moved to another system.
        raise EnvironmentError(
            "Wheels are not supported with setuptools version < 18!"
        )
    if python_version < (3, 5):
        requires.append("typing")
        requires.append("pathlib2")
    if python_version < (3, 4):
        requires.append("enum34")


setuptools.setup(
    name="PyPWA",
    version=__version__,
    author=__author__,
    author_email=__email__,
    packages=setuptools.find_packages(),
    url="http//pypwa.jlab.org",
    license=__license__,
    description="General Partial Wave Analysis",
    test_suite="tests",
    entry_points=entry_points,
    keywords="PyPWA GeneralFitting Partial Wave Analysis Minimization",
    install_requires=requires,
    tests_require=tests,
    extras_require=extras,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)
