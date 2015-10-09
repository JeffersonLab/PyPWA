__author__ = "Mark Jones"
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Alpha.0"

from setuptools import setup, find_packages

setup(
	name="PyPWA",
	version=__version__+"-"+__status__,
	author="PyPWA Team",
	author_email="someone@jlab.org",
	packages=find_packages(),
	url="http//pypwa.jlab.org",
	license="MIT License",
	description="General Partial Wave Analysis",
	entry_points={
		"console_scripts": [
			"GeneralFitting = PyPWA.entry.console:Lets_Get_Fit",
		],
	},
	keywords = "PyPWA GeneralFitting Partial Wave Analysis Minimalization",
	install_requires=[
	"iminuit<2.0",
	"numpy<2.0",
	"pyyaml<4"
	],
	classifiers=[
	"Development Status :: 3 - Alpha",
	"Environment :: Console",
	"Intended Audience :: Science/Research",
	"License :: OSI Approved :: MIT License",
	"Natural Language :: English",
	"Operating System :: POSIX :: Linux",
	"Programming Language :: Python :: 2.7",
	"Topic :: Scientific/Engineering :: Mathematics",
	"Topic :: Scientific/Engineering :: Physics",
	],
)
