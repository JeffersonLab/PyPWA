

Processing Module
=================
PyPWA's processing module is a simple OpenMP inspired processing module based 
off of Python's multiprocessing module. It's designed for use with numpy flat
array data and should be able to utilize every physical core on your machine,
but has mixed performance with Intel's Hyperthreading implementation.


Using Processing
----------------
This plugin doesn't offer many adjustable options from the configuration file
since most of the functionality of the plugin is automated for the ease of the
user.

Processing Options
^^^^^^^^^^^^^^^^^^
To use the default processing module with your shell main if it supports it,
add the plugin to your configuration.

The name of the plugin is 'Builtin Multiprocessing' and has the option:

- number of processes

  - not required
  - if omitted will default to the number of available processes on the
    physical machine.

Processing Configuration Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none
   :linenos:

   Builtin Multiprocessing:
      number of processes: 4
