#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016  JLab
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

import setuptools

__author__ = "PyPWA Team and Contributors"
__license__ = "GPLv3"
__version__ = "3.0.0.dev"
__email__ = "pypwa@jlab.org"
__status__ = "development"


progs = "PyPWA.progs"

entry_points = {
    "console_scripts": [
        f"pydata = {progs}.data:data",
        f"pybin = {progs}.binner:start_binning",
        f"pysimulate = {progs}.simulation:simulation"
    ]
}

requires = [
    "tqdm",          # Progress Bars
    "iminuit<2.0",   # Default minimizer
    "scipy",         # Needed for Nestle with multiple ellipsoids.
    "numpy>1,<2.0",  # Arrays and optimizations
    "pyyaml",        # YAML Parser
    "tabulate",      # Tables for iminuit
    "appdirs",       # Attempts to find data locations
    "tables"       # Stores table in a specialized table format
]

extras = {
    # Adds value correction to users configuration file
    "fuzzing": ["fuzzywuzzy", "python-Levenshtein"]
}

tests = [
    'pytest',
    'pytest-runner',
    "pytest-cov"
]


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
