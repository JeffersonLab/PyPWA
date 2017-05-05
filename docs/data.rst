

Data Module
===========
PyPWA's data module is the core builtin module that is used to load and
iterate over data files for PyPWA. The module is capable of reading and
writing single arrays to text files along with full structured arrays in EVIL
Format, CSV, TSV, and GAMP data.

.. note::
   More file formats can be defined by the user relatively easily, see
   `Extending the Data Module`_ for more information.


Using Data
----------
The plugin itself is loaded internally as two separate plugins, the 'Builtin
Parser' and 'Builtin Reader'. The main difference is that the parser loads
all of the data from the file into RAM then caches the results, while the
reader will only load a single event from the file at a time.

.. note::
   Although 'Builtin Parser' and 'Builtin Reader' are defined in the same
   module, and are closely related to each other, they are not interchangeable
   as they expose different interfaces for the shell module to interact with.


Data Options
^^^^^^^^^^^^
To use either the parser or the iterator and your shell plugin supports it,
add it to your configuration. However, make sure to select the correct
plugin, as the parser and iterator can not be interchanged.

To use the parser add the name 'Builtin Parser' to your configuration file,
along with any of the optional options:

- enable cache

  - Not required, optional
  - defaults to True
  - Defines whether the cache should be enabled or not, this is generally
    safe to leave on as the plugin is smart enough to detect changes in the
    file before using the cache. Should only be tuned off if there is nowhere
    for the plugin to write cache data.
- clear cache

  - Not required, advanced
  - Defaults to False
  - Will forcefully clear the cache off all data files that are loaded by the
    plugin, though will still create a cache after the data is loaded unless
    'enable cache' is set to False as well.
- user plugin

  - Not required, advanced
  - Defaults to None
  - Adds the specified file or directory to the plugin search path. If there
    are any plugins in the directory that extended the data modules
    interfaces for data parsers, they will be loaded as a potential data
    parser and writer for the files. For more information, see
    `Extending the Data Module`_


To use the iterator, add the name 'Builtin Reader' to your configuration
file, along with any of the optional options:

- fail

  - Not required, advanced
  - Defaults to False
  - Forces the program to crash if it fails to iterator over a file even if
    another method of loading the data exists, this should be left on False
    unless you know what you are doing.
- user plugin

  - Not required, advanced
  - Defaults to None
  - Adds the specified file or directory to the plugin search path. If there
    are any plugin in the directory that extended the data modules interfaces
    for data iterators, they will be loaded as a potental data reader and
    writer for the files. For more information, see `Extending the Data Module`_


Data Configuration Example
^^^^^^^^^^^^^^^^^^^^^^^^^^
The builtin parser inside the configuration:

.. code-block:: none
   :linenos:
      
   Builtin Parser:
      enable cache: True
      clear cache: False
      user plugin:

The builtin reader inside the configuration:

.. code-block:: none
   :linenos:
      
   Builtin Reader:
      fail: False
      user plugin:


Extending the Data Module
-------------------------
A truly great explanation of the greatest of the great plugins.
