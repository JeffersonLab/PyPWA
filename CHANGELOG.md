# Changelog
All changes important to the user will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)

## [Unreleased]
### Added
 - ProjectDatabase has been added handle large data manipulation on disk
   instead of in memory.
 - Reader/Writer now share path of the file being operated on.
 - Binning now works in both fixed count and ranges, and can be done
   entirely in memory.
 - Initial Jupyter and IPython support.
 - Adding lego plotting.
 - Likelihoods are now standalone objects that can be combined with any
   optimizer.
 - Resonance support now builtin using DataFrames as a backbone.
   Resonances are now saved as a two sheet excel file, and can be modified
   using the supplied wave and resonance objects.
 - Adds support for Numexpr to accelerate computation.
 - Simulation can be done as two separate parts through PyPWA.simulate
 - Github Templates to help users and developers contribute to PyPWA
### Changed
 - Separate release tag from version info
 - Package info is now stored in PyPWA.info
 - pydata has officially been updated to PyPWA 3.0.
 - Structured Arrays have been replaces for Pandas DataFrames.
 - Reactions have been merged into ParticlePool.
 - Vectors have been simplified to be easier to test while still being
   powerful to use.
 - ProcessInterfaces now must be closed after use. This includes all
   Likelihood objects.
 - Cache has been refactored to be easier to be completely usable by
   itself.
### Removed
 - SlotTable has been removed in favor of Project. Both use PyTables
   for the backend.
 - Unsupported Python versions removed from package's classifiers.
### Fixed
 - GAMP no longer claims that it can read PF files.
 - Cache will correctly report invalid when it's contents differ from the
   source file.
 - monte_carlo_simulation and likelihoods now correctly handle exceptions
   that occur in the child processes.
 - Pipes are correctly closed now.
 - Extended Log-likelihood is now correctly calculated
 - Sv Writer will now write data.
 - Kv Reader will now read data.

## [3.0.0a1] - 2019-6-17
### Added
 - Added numpy reader and writer.
 - Adds a helper script to clean the project directory of caches.
 - Adds initial documentation for PyPWA.
 - Added support for 3 Vectors, 4 Vectors, and Particles
 - Added ParticlePool to aid in working with multiple Particles
 - Added a binning utility that supports multiple binning variables and
   dimensions
 - Added PyTables support, so that large datasets can be easily managed
### Changed
 - All program names have been lowercased
 - Configuration package has been compressed into a single module
 - PySimulate now is a library that has no UI, and has a UI portion
   that exclusively works with interfacing
 - Fuzzywuzzy is now optional
 - Process package is now a single module. Interface no longer uses IS_DUPLEX
 - Bulk of program functionality moved to libs, progs being just for UI
 - Builtin Plugins moved to libs, old plugin's plugins have still reside
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
 - The user can AND, OR, or XOR masks together with PyMask
### Changed
 - Removed previous_event from Process Interface
 - Duplex Pipes are used over Simplex Pipes for Duplex Processes
 - Changes get_file_length to using a binary buffered search.
 - Moved PyPWA.core.shared to PyPWA.libs
 - Split interface's plugins and internals to their own separate file based
   on the interfaces purpose.
 - PyFit no longer assumes bins are named 'BinN' you must specify Bin names 
   in 'internal data'.
 - Multiplier effect for the Minimizers has been moved to the individual
   likelihoods.
 - PyMask defaults to AND operations instead of or now.
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
 - Masking utility 'PyMask' to mask and translate data
### Changed
 - Plugin Loader now returns initialized objects
 - Renamed shell to progs
 - Moved all shell related items into a package called shell inside progs
 - Renamed CHANGELOG.mg to CHANGELOG.md
 - Renamed 'blank shell module' to 'blank program module'
 - Removed support for boolean and float arrays from EVIL Parser
 - Renamed internal GAMP type to Tree type
 - Split flat data into Columned data and standard arrays
### Fixed
 - ChiSquare and Empty likelihoods are now actually usable
 - Setup.py would fail on setuptools versions < 20

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


[Unreleased]: https://github.com/JeffersonLab/PyPWA/compare/v3.0.0a1...development
[3.0.0a1]: https://github.com/JeffersonLab/PyPWA/compare/v2.2.1...v3.0.0a1
[2.2.1]: https://github.com/JeffersonLab/PyPWA/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/JeffersonLab/PyPWA/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/JeffersonLab/PyPWA/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/JeffersonLab/PyPWA/compare/v1.1...v2.0.0
