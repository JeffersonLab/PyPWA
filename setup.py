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

import os
import setuptools
from distutils.extension import Extension
from pathlib import Path

import numpy as np

try:
    from Cython.Distutils import build_ext
except ImportError:
    print("Install Cython before building!")
    raise


__author__ = "PyPWA Team and Contributors"
__license__ = "GPLv3"
__version__ = "3.2.0"
__email__ = "pypwa@jlab.org"
__status__ = "development"


"""
Why are these entry points disable?

So PyPWA 2.0 had support for running scripts directly from the local
directory, and these entry points were that functionality. With PyPWA 3
though we dumped these scripts and instead moved almost entirely to
Jupyter notebooks since they offer a solid amount of flexibility for
physicists without the complicated overhead of importing Python scripts
into an already running interpreter. Maybe eventually we'll fully remove
them, bring them back if the physicists want them, or roll out other
helping utilities like pymask if they need it.
"""


progs = "PyPWA.progs"
entry_points = {
    "console_scripts": [
        f"pymask = {progs}.masking:start_masking",
#        f"pybin = {progs}.binner:start_binning",
#        f"pysimulate = {progs}.simulation:simulation",
#        f"pyfit = {progs}.pyfit:start_fitting"
    ]
}

extension_kwargs = {
    "sources": [],
    "language": "c++",
    "extra_compile_args": {
        "gcc": ["-Wall", "-std=c++11", "-fPIC"],
        "include_dirs": [np.get_include()]
    }
}


setup_kargs = {
    "name": "PyPWA",
    "version": __version__,
    "author": __author__,
    "author_email": __email__,
    "packages": setuptools.find_packages(),
    "url": "http://pypwa.jlab.org",
    "license": __license__,
    "ext_module": [Extension("_lib", **extension_kwargs)],
    "description": "General Partial Wave Analysis",
    "test_suite": "tests",
    "entry_points": entry_points,
    "keywords": "PyPWA GeneralFitting Partial Wave Analysis Minimization",
    "install_requires": [
        "cython",      # C/C++ Optimizations
        "tqdm",        # Progress Bars
        "iminuit",     # Default minimizer
        "scipy",       # Needed for Nestle with multiple ellipsoids.
        "numpy",       # Arrays and optimizations
        "pyyaml",      # YAML Parser
        "tabulate",    # Tables for iminuit
        "appdirs",     # Attempts to find data locations
        "tables",      # Stores table in a specialized table format
        "pandas",      # A powerful statistics package that's used everywhere
        "openpyxl",    # Provides support for XLXS, used for resonance,
        "matplotlib",  # Adds support for plotting
        "numexpr"      # Accelerates numpy by removing intermediate steps
    ],
    "test_require": [
        'pytest',
        'pytest-runner',
        "pytest-cov"
    ],
    "extras_requires": {"fuzzing": ["fuzzywuzzy", "python-Levenshtein"]},
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    "zip_safe": False
}


"""
Anaconda doesn't have NVCC, but it does supply all the other
required libraries. Also, if there are no CUDA libs on the system
(No NVIDIA GPU) then CUDA integration will be disabled.
"""

base_dir = None
for directory in os.environ["PATH"].split(os.pathsep):
    if Path(directory + "/nvcc").exists():
        nvcc_location = Path(directory + "/nvcc")
        base_dir = Path(os.environ["CONDA_PREFIX"])
        break

if base_dir and base_dir.exists() and False:
    print("Compiling with CUDA support.")

    class custom_build_extension(build_ext):

        def build_extensions(self):
            self.src_extensions.append(".cu")
            default_compiler_so = self.compiler_so
            comp = self._compile

            def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
                if os.path.splitext(src)[1] == '.cu':
                    self.set_executable('compiler_so', str(nvcc_location))
                    postargs = extra_postargs["nvcc"]
                else:
                    postargs = extra_postargs["gcc"]

                comp(obj, src, ext, cc_args, postargs, pp_opts)
                self.compile_so = default_compiler_so

            self._compile = _compile
            build_ext.build_extensions(self)

    extension_kwargs["sources"] = []
    extension_kwargs["libraries"] = ["cudart"]
    extension_kwargs["runtime_library_dirs"] = base_dir / "lib64"
    extension_kwargs["extra_compile_args"]["nvcc"] = [
        "-fPIC", "--ccbin gcc", "-shared", "-arch=sm_61",
        "-gencode=arch=compute_61,code=sm_61",
        "-gencode=arch=compute_70,code=sm_70",
        "-gencode=arch=compute_70,code=compute_70",
        "-gencode=arch=compute_75,code=sm_75",
        "-gencode=arch=compute_75,code=compute_75"
    ]
    extension_kwargs["extra_compile_args"]["include_dirs"].append(
        base_dir / "include"
    )
    setup_kargs["ext_module"].append(Extension("_cuda", **extension_kwargs))
    setup_kargs["cmdclass"] = {"build_ext": custom_build_extension}


setuptools.setup(**setup_kargs)
