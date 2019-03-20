# Changelog
All changes important to the user will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)


## [Unreleased]
### Added
 - Added numpy reader and writer.
 - Adds a helper script to clean the project directory of caches.
 - Adds initial documentation for PyPWA.
 - Adds a python shell interface to data processor to avoid the configuration
   database
 - Added support for 3 and 4 vector data
 - Added Particle and ParticlePool to aid in working with particle data
 - Configurator gained support for Dictionaries nested inside a list
 - Added a binning utility that supports multiple binning variables and
   dimensions
 - Added PyTables support, so that large datasets can be easily managed
### Changed
 - Moved the program plugins, data plugin, and processing plugin to components
 - Moved Nestle and Minuit to the Optimizer component
 - Renamed 'Builtin Multiprocessing' to 'Multiprocessing'
 - Renamed 'Builtin Parser' and "Builtin Iterator" to "Data Processor"
 - Combined iterator and parsing objects to allow easy fallback
 - All components now exist inside PyPWA.libs.components
 - GAMP was updated to use Particles and ParticlePool
 - Data Processor no longer uses data to choose a writer, instead uses boolean
   flags to determine whether to use particle, flat, or columned writer.
 - If there is no function to write when generating the configuration, then
   writing the function file will be skipped.
### Removed
 - Nestle Minimization. There is currently no clear way to have Minuit and
   Nestle to operate with each other nicely. Implementation for multiple
   optimizers will remain, as well as new associated issues created.
 - Removed support for all version of Python before 3.7
### Fixed
### Security


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
 - Multipler effect for the Miminzers has been moved to the individual
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


[Unreleased]: https://github.com/JeffersonLab/PyPWA/compare/v2.2.1...development
[2.2.1]: https://github.com/JeffersonLab/PyPWA/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/JeffersonLab/PyPWA/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/JeffersonLab/PyPWA/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/JeffersonLab/PyPWA/compare/v1.1...v2.0.0
