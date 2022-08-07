# Changelog

All changes important to the user will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)


## [4.0.0] - Unreleased (PyPWA-Next)
### Added
- Anaconda environments. There are two anaconda environments included
  inside the source folder at the moment. `anaconda-environment.yml` and
  `dev-environment.yml`. These should provide a nice starting point for
  anyone wanting to work on or with PyPWA. Pull requests are welcomed
  if you think a package should be added to the base environment.
- Added PyTorch for GPU and Apple Metal support. Can be specified during
  install using `pip install pypwa[torch]`. Amplitude support is specified
  by setting the `USE_TORCH` flag to True.
- Added support for Python's Multithreading. You should only use this when
  computation is happening on separate nodes and/or your optimizer choice
  does not support passing it's values across an OS Pipe.
- Added support for Minuit's parameter array argument. Now amplitudes can
  be written to accept a single array containing all the array values.
- Debugging support for amplitudes is now explicit. You can set the `DEBUG`
  flag to True on your amplitude before simulation or fitting, and it'll run
  in the main process so traceback and errors will not be suppressed.
- Amplitudes can now know where they live. Amplitudes have a `THREAD` flag
  that is numbered from 0 to N-threads that will specify which thread the
  amplitude is running in. This is useful if you want to pair your
  processes/threads with external devices like GPUs or OpenMPI nodes.
### Changed
- Data module will no longer bury the Cache object. The cache object will
  now reside in the same directory as the parsed data.
- Moves Emcee to an optional dependency so that PyPWA can function in a
  base anaconda environment. If Emcee is installed, or if emcee is
  specified during installation using `pip install pypwa[emcee]`, the
  emcee functionality will be usable.
- iMinuit has changed their ABI entirely, so the iminuit function has
  been changed to adapt to the new ABI.
- Updated all dependencies around ReadTheDocs to avoid GitHub flagging
  the dependencies for exploits.
### Removed
- Project manager. There were several bugs throughout the module, and as
  far as we are aware, no users using the module. If you're affected by
  this change, please open an issue in the issue tracker to let us know.
- Removed the **command line** Binning utility. The Jupyter-based and
  internal binning utilities remain unaffected. If this affects you,
  please open an issue.
- Removed appdirs as a dependency.
- Removed CuPy support, replaced by PyTorch.
- Removed PyYaml Configuration support.
### Fixed
- The bin by range function was not sampling data correctly. The intended
  behaviour was for each bin to be sampled by N samples, and then those
  samples to be shuffled to add randomization. However, because the
  shuffling was improperly implemented, what would occur instead is a single
  random event would be dropped from the sample, and then returned. This
  no longer occurs, and the returned bins will now be the correct length, 
  and will be correctly shuffled.


## [3.4.0] - 2021-7-23
### Added
- Peter's emcee wrapper, available at PyPWA.mcmc
### Changed
- System tests are now located in tests/system_tests
- PyMask will now return exit values on call
### Removed
- PySimulate has been removed since it was limited in use, and it's
  functionality has been consumed by the PyPWA scripting libs.
  

## [3.3.0] - 2021-6-20
### Added
- 2D Gauss introductory tutorial to the documentation
- CuPy support for Likelihoods and Simulation. This means we now officially
  support NVIDIA GPU acceleration, however for now it is limited to a single
  GPU. If there is enough demand for this to be expanded on, support for 
  multiple GPUs will be added.
### Changed
- Particle now requires a charge to be supplied during the creation of the
  object. GAMP has also been modified to support the Charge being passed
  through to the Particle
- Depreciated internal options that were passed to Minuit have been
  replaced with the modern alternatives.
## Fixed
- Likelihoods were spawning multiple processes even when USE_MP was set
  to false. This has been corrected, and will avoid spawning extra
  processes as it was intended. 

## [3.2.3] - 2021-6-11
### Added
- Particle Pools can now compared against other Particle Pools to see if they
  are storing the same content.
### Fixed
- Regression from 3.2.0 where Gamp would not write out data to disk. This time
  by wrapping the data in a float, which should catch instances where the value
  stored is a pure scalar, verses instances where the data is an array with a
  len == 1

## [3.2.2] - 2021-6-11
### Fixed
- Particles can now be masked again, the mask is no longer silently deleted
  when passed to the object.
- Numpy's warning about numpy.float being deprecation should be resolved.
- Any warnings about the LaTeX in the Likelihood's Docstrings being
  deprecated should be resolved as well.

## [3.2.1] - 2021-6-10
### Fixed
- Gamp no longer combines particles with the same ID
- Fixed issue where display_raw would fail in Jupyter with Particles

## [3.2.0] - 2021-6-1
### Added
- Vectors now support iPython and Jupyter Pretty printing
### Changed
- Vector sanitization function has improved handling of non-array inputs
### Fixed
- FourVectors variable order is now in the correct order
- Vectors now work with inputs that aren't arrays
- Patched issue with GAMP failing to write to file

## [3.1.0] - 2020-10-2
### Added
- Helper functions `pwa.pandas_to_numpy` to convert Pandas data types to
  Numpy Structured Arrays, and `pwa.to_contiguous` to convert DataFrames
  and Structured Arrays columns to contiguous arrays for quicker
  processing and C/Fortran Support
- New experimental file format ParticleGZ, a direct-to-memory file format
  using pickle, csv, and Tar/GZ to compress data into a single archive for
  easy use.
- Reference documentation to the Read The Docs for the various modules
  in PyPWA.
- Initial examples section added.
### Changed
- Users now have to option to request structured Numpy arrays or Pandas
  DataFrames from `pwa.read` and `pwa.get_reader`
- `pwa.cache` now defaults to intermediate caching, and has to be disabled
  for use with caching files
- Vectors str and repr field now output the mean of their theta, phi, as well
  as particle id and mass if they are available.
- Vectors now wrap individual numpy arrays instead of a single structured
  array or DataFrame. This was done to improve performance of the vector
  as well as to make it C contiguous.
### Fixed
- `pwa.write` would fail to write CSV Numpy Arrays
- `pwa.write` would occasionally fail to detect DataFrames
- Vectors would occasionally replace their fields with just their x values.

## [3.0.0] - 2020-6-4
### Added
- `ProjectDatabase` has been added handle large data manipulation on disk
  instead of in memory.
- Reader/Writer now share path of the file being operated on.
- Binning now works in both fixed count and ranges, and can be done
  entirely in memory.
- Initial Jupyter and IPython support.
- Adding lego plotting.
- Likelihoods are now standalone objects that can be combined with any
  optimizer.
- Resonance support now builtin using `DataFrames` as a backbone.
  Resonances are now saved as a two sheet excel file, and can be modified
  using the supplied wave and resonance objects.
- Adds support for `Numexpr` to accelerate computation.
- Simulation can be done as two separate parts through `PyPWA.simulate`
- Github Templates to help users and developers contribute to PyPWA
### Changed
- Separate release tag from version info
- Package info is now stored in `PyPWA.info`
- `pydata` has officially been updated to PyPWA 3.0.
- Structured Arrays have been replaces for Pandas `DataFrames` in some
  cases. Vectors still based on `numpy` arrays to maintain performance.
- Reactions have been merged into `ParticlePool`.
- Vectors have been simplified to be easier to test while still being
  powerful to use.
- `ProcessInterfaces` now must be closed after use. This includes all
   Likelihood objects.
- `pwa.data` has been refactored to be easier to be completely usable by
  itself.
### Removed
- `SlotTable` has been removed in favor of `Project`. Both use `PyTables`
  for the backend.
- Unsupported Python versions removed from package's classifiers.
### Fixed
- GAMP no longer claims that it can read PF files.
- Cache will correctly report invalid when it's contents differ from the
  source file.
- `monte_carlo_simulation` and likelihoods now correctly handle exceptions
  that occur in the child processes.
- Pipes are correctly closed now.
- Extended Log-likelihood is now correctly calculated
- Sv Writer will now write data.
- Kv Reader will now read data.

## [3.0.0a1] - 2019-6-17
### Added
- Added `numpy` reader and writer.
- Adds a helper script to clean the project directory of caches.
- Adds initial documentation for PyPWA.
- Added support for 3 Vectors, 4 Vectors, and Particles
- Added `ParticlePool` to aid in working with multiple Particles
- Added a binning utility that supports multiple binning variables and
  dimensions
- Added `PyTables` support, so that large datasets can be easily managed
### Changed
- All program names have been lowercased
- Configuration package has been compressed into a single module
- `PySimulate` now is a library that has no UI, and has a UI portion
  that exclusively works with interfacing
- `Fuzzywuzzy` is now optional
- Process package is now a single module. Interface no longer uses
  `IS_DUPLEX`
- Bulk of program functionality moved to libs, progs being just for UI
- Builtin Plugins moved to `libs`, old plugin's plugins have still reside
  in plugins, but under a package with the appropriate name. I.E. data
  plugins are in plugins/data.
- All file related libs have been moved to libs/file
- Combined optimizers with fit library
- GAMP was updated to use Particles and ParticlePool
- Files with extra newline should parse correctly now
- CSV and TSV files will be lf instead of crlf on linux systems now
### Removed
- Nestle Minimization. There is currently no clear way to have Minuit and
  Nestle to operate with each other nicely. Implementation for multiple
  optimizers will remain, as well as new associated issues created.
- Removed support for all version of Python before 3.7

## [2.2.1] - 2017-10-16
### Fixed
- Setup would pull in unstable Yaml parser

## [2.2.0] - 2017-7-26
### Added
- Process Plugin support for List Data
- Adds Exception handling to Processes
- PyMask support for multiple masking files.
- PyFit will now filter out events if the Bin value is 0
- The user can `AND`, `OR`, or `XOR` masks together with PyMask
### Changed
- Removed previous_event from Process Interface
- Duplex Pipes are used over Simplex Pipes for Duplex Processes
- Changes `get_file_length` to using a binary buffered search.
- Moved `PyPWA.core.shared` to `PyPWA.libs`
- Split interface's plugins and internals to their own separate file based
  on the interfaces purpose.
- PyFit no longer assumes bins are named `'BinN'` you must specify Bin
  names in `'internal data'`.
- Multiplier effect for the Minimizers has been moved to the individual
  likelihoods.
- PyMask defaults to `AND` operations instead of `OR` now.
### Fixed
- PyFit will now shutdown correctly when killed with Ctrl-C or other
  interrupt.
- The ChiSquared will no longer be multiplied by -1 when being minimized.
- Data Parser's Cache would crash on very large files.

## [2.1.0] - 2017-6-30
### Added
- Argument Parser for simple programs where a configuration file would be
   unneeded overhead for the user.
- Numpy Data support for single arrays and pass fail files.
- Data Plugin now has two array types, Single Array and Columned Array
- Memory and Iterator objects now imported into PyPWA
- Iterators report length now
- Masking utility `PyMask` to mask and translate data
### Changed
- Plugin Loader now returns initialized objects
- Renamed `shell` to `progs`
- Moved all shell related items into a package called shell inside progs
- Renamed `CHANGELOG.mg` to `CHANGELOG.md`
- Renamed 'blank shell module' to 'blank program module'
- Removed support for boolean and float arrays from EVIL Parser
- Renamed internal GAMP type to Tree type
- Split flat data into Columned data and standard arrays
### Fixed
- ChiSquare and Empty likelihoods are now actually usable
- `setup.py` would fail on `setuptools` versions < 20

## [2.0.0] - 2017-6-5
### Added
- Plugin Subsystem
- Configurator Subsystem
- Data Plugin
- SV Plugin
- EVIL Plugin
- GAMP Plugin
- Data Caching
- Processing Plugin
- iMinuit plugin
- Nestle likelihood
- PyFit plugin
- Log Likelihood Plugin
- Chi-Squared Likelihood
- PySim plugin
- Packaging

[Unreleased]: https://github.com/JeffersonLab/PyPWA/compare/v3.3.0...main
[3.3.0]: https://github.com/JeffersonLab/PyPWA/compare/v3.2.2...v.3.2.3
[3.2.3]: https://github.com/JeffersonLab/PyPWA/compare/v3.2.2...v.3.2.3
[3.2.2]: https://github.com/JeffersonLab/PyPWA/compare/v3.2.1...3.2.2
[3.2.1]: https://github.com/JeffersonLab/PyPWA/compare/v3.2.0...v3.2.1
[3.2.0]: https://github.com/JeffersonLab/PyPWA/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/JeffersonLab/PyPWA/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/JeffersonLab/PyPWA/compare/v3.0.0a1...v3.0.0
[3.0.0a1]: https://github.com/JeffersonLab/PyPWA/compare/v2.2.1...v3.0.0a1
[2.2.1]: https://github.com/JeffersonLab/PyPWA/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/JeffersonLab/PyPWA/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/JeffersonLab/PyPWA/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/JeffersonLab/PyPWA/compare/v1.1...v2.0.0
