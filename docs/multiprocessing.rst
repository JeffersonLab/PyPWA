

PyPWA's Multiprocessing Module
==============================
PyPWA's processing module is a simple OpenMP inspired processing module based 
off of Python's multiprocessing module. It's designed for use with numpy flat
array data and should be able to utilize every physical core on your machine,
but has mixed performance with Intel's Hyperthreading implimentation.


User Documentation
------------------
This plugin doesn't offer many adjustable options from the configuration file
since most of the functionality of the plugin is automated for the ease of the
user.

Configurator Options
^^^^^^^^^^^^^^^^^^^^
To use the default processing module with your shell main if it supports it,
add the plugin to your configuration.

The name of the plugin is 'Builtin Multiprocessing' and has the option:

- number of processess
  - not required 
  - if omitted will default to the number of available processes on 
    the physical machine.

Example
^^^^^^^
.. codeblock:: yml
   :linenos:

   Builtin Multiprocessing:
      number of processes: 4
