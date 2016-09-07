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
__license__ = "MIT"
__version__ = "2.0.0-beta.2"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "beta"


setup(
    name="PyPWA",
    version=__version__+"-"+__status__,
    author="PyPWA Team",
    author_email="maj@jlab.org",
    packages=find_packages(),
    url="http//pypwa.jlab.org",
    license="MIT License",
    description="General Partial Wave Analysis",
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "GeneralFitting = PyPWA.entries.shell:general_fitting",
            "LikelihoodFitting = PyPWA.entries.shell:likelihood_fitting",
            "ChiSquaredFitting = PyPWA.entries.shell:chi_squared",
            "PySimulator = PyPWA.entries.shell:simulator",
            "GenerateIntensities = PyPWA.entries.shell:intensities",
            "GenerateWeights = PyPWA.entries.shell:rejection_method"
        ]
    },
    keywords="PyPWA GeneralFitting Partial Wave Analysis Minimization",
    install_requires=[
        "iminuit<2.0",
        "numpy<2.0",
        "ruamel.yaml",
        "tabulate",
        "appdirs",
        "fuzzywuzzy",
        "python-Levenshtein"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', "pytest-cov", "pytest-logging"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)

