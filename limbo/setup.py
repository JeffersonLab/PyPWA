__author__ = "Mark Jones"
__license__ = "MIT"
__version__ = "2.0.0b1"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "beta"

from setuptools import setup, find_packages

setup(
    name="PyPWAiSOBAR",
    version="1.0.0",
    author="PyPWA Team",
    author_email="maj@jlab.org",
    packages=find_packages(),
    url="http//pypwa.jlab.org",
    license="MIT License",
    description="General Partial Wave Analysis",
    install_requires=[
        "iminuit",
        "numpy",
        "matplotlib",
        "numexpr"
    ],
    entry_points={
        "console_scripts": "GampMasker = PyPWAiSOBAR.generalShell.utilities.gampMasker:run_gamp_masker"
    }
)

