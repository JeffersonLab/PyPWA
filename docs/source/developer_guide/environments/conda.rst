
********
Anaconda
********
Anaconda is a distribution of python that specializes in data analysis.
It makes installing PyPWA dependencies significantly easier than managing
on your local machine.

Getting Anaconda
================
There are two versions available of Anaconda, the full Anaconda installation
that is 10+ Gb in size, or an alternative smaller Miniconda. PyPWA will work
with either installation. We recommend that you pick the Python 3 variant.

`Anaconda Download <https://www.anaconda.com/download>`_

`Miniconda Download <https://conda.io/miniconda.html>`_

After you download Anaconda, mark the binary as executable, then run
the resulting file. You should be greeted with an installer. Follow the on
screen instructions.


Creating the conda environment
==============================
After you install Anaconda, you should change directory into the PyPWA source
directory, then run:

.. code-block:: sh

  conda create -p venv python=3 scipy numpy cython ipython jupyter pyqt \
    matplotlib pytest sphinx
  source activate venv
  pip install -e .

This should give you a working Anaconda Virtual Environment with PyPWA
inside it.

To activate the environment all you have to do is:

.. code-block:: sh

  source activate venv

and to deactivate all you need to do is run:

.. code-block:: sh

  source deactivate
