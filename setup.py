__author__ = "Mark Jones"
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0.0.2"

from setuptools import setup, find_packages

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
            "GeneralFitting = PyPWA.entry.console:start_console_general_fitting",
            "GeneralSimulator = PyPWA.entry.console:start_console_general_simulator",
            "GenerateIntensities = PyPWA.entry.console:start_console_general_intensities",
            "GenerateWeights = PyPWA.entry.console:start_console_general_weights",
            "GeneralChiSquared = PyPWA.entry.console:start_console_general_chisquared"
        ]
    },
    keywords="PyPWA GeneralFitting Partial Wave Analysis Minimization",
    install_requires=[
        "iminuit<2.0",
        "numpy<2.0",
        "pyyaml<4",
        "tabulate"
    ],
    setup_requires=['pytest-runner', 'pytest-cov'],
    tests_require=['pytest'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)

