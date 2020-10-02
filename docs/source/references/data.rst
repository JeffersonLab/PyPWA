
=================
Working with Data
=================


Reading and Writing Data
========================

This is the reference documentation for the functions and classes
inside PyPWA that can be used for parsing and writing data to disk.
There exists four different methods to do so:

* :ref:`Reading and Writing Data<reading>`
* :ref:`Data Iterators and Writers<iterator>`
* :ref:`Working with HDF5<hdf5>`
* :ref:`Caching<caching>`

PyPWA also defines a vector data types and collections for working with
Particles, Four Vectors, and Three Vectors, which can be found
:ref:`here.<vectors>`


.. _reading:

Reading and Writing Data
------------------------

Reading and writing from disk to memory. This method will load the entire
dataset straight into RAM, or write a dataset straight from RAM  onto disk.

.. autofunction:: PyPWA.read
.. autofunction:: PyPWA.write


.. _iterator:

Data Iterators and Writers
--------------------------

Reading and writing a single event at a time instead of having the entire
contents of the dataset memory at once. This is good choice if you are
wanting to rapidly transform the data that is on disk.

.. autoclass:: PyPWA.DataType
   :members:

.. autofunction:: PyPWA.get_writer
.. autofunction:: PyPWA.get_reader


.. _hdf5:

Working with HDF5
-----------------

Working directly with HDF5 datasets. These datasets offer massive speed
advantages over traditional flat files, have a lot of development time
put behind them by the HDF group, offer chunk loading, and on the fly
data compression.

.. autoclass:: PyPWA.ProjectDatabase
   :members:


.. _caching:

Caching
-------

Using pickles to quickly write and read data straight from disk as
intermediate caching steps. These are special functions that allow caching
values or program states quickly for resuming later. This is a good way to
save essential data for a Jupyter Notebook so that if the kernel is
rebooted, data isn't lost.

.. autofunction:: PyPWA.cache.read
.. autofunction:: PyPWA.cache.write



Binning
=======

We provide functions that make binning data in memory an easy process,
however for HDF5 a future more in-depth example and documentation
will be made available.

.. autofunction:: PyPWA.bin_with_fixed_widths
.. autofunction:: PyPWA.bin_by_range


.. _vectors:

Builtin Vectors
===============

PyPWA includes support for both 3 and 4 vector classes, complete with
methods to aid operating with vector data. Each vector utilizes Numpy
for arrays and numerical operations.

.. autoclass:: PyPWA.ParticlePool
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: PyPWA.Particle
   :members:
   :inherited-members:

.. autoclass:: PyPWA.FourVector
   :members:
   :inherited-members:

.. autoclass:: PyPWA.ThreeVector
   :members:
   :inherited-members:
