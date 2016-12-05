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

from setuptools import setup, find_packages

__author__ = "Mark Jones"
__license__ = "GPLv3"
__version__ = "2.0.0-rc4"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "development"


setup(
    name="PyPWA",
    version=__version__,
    author="PyPWA Team",
    author_email="maj@jlab.org",
    packages=find_packages(),
    url="http//pypwa.jlab.org",
    license=__license__,
    description="General Partial Wave Analysis",
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "PyFit = PyPWA.entries.shell:general_fitting",
            "LikelihoodFit = PyPWA.entries.shell:likelihood_fitting",
            "ChiSquaredFit = PyPWA.entries.shell:chi_squared",
            "PySimulate = PyPWA.entries.shell:simulator",
            "GenerateIntensities = PyPWA.entries.shell:intensities",
            "GenerateWeights = PyPWA.entries.shell:rejection_method"
        ]
    },
    keywords="PyPWA GeneralFitting Partial Wave Analysis Minimization",
    install_requires=[
        "typing",       # Support for function typing
        "iminuit<2.0",  # Default minimizer
        "numpy<2.0",    # Arrays and optimizations
        "ruamel.yaml",  # Advanced YAML Parser
        "tabulate",     # Great aesthetic tables
        "appdirs",      # Attempts to find data locations
        "fuzzywuzzy",   # Fuzzes the user input
        "python-Levenshtein"
    ],
    extras_require={
        'multinest': ["pymultinest"]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', "pytest-cov", "pytest-logging"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)
