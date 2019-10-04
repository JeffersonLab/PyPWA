
############
Installation
############

PyPWA can be installed with ``pip`` or ``conda`` with Python 3.7 or newer



Conda
#####

**(Optional) Setup an environment**

.. code-block:: sh

   conda create -n pypwa python=3
   conda activate pypwa

**Install dependencies**

.. code-block:: sh

   conda install tqdm iminuit numpy pyyaml tabulate appdirs pytables numba

**Fetch the latest version of PyPWA and install**

.. code-block:: sh

   git clone --depth=1 https://github.com/JeffersonLab/PyPWA.git
   cd PyPWA
   pip install .


**(Optional) Install Fuzzywuzzy**

Fuzzywuzzy allows for minor issues in configuration files to be corrected,
such as simple mistypes, minor misspelling, or case errors.

.. code-block:: sh

   conda install -c conda-forge fuzzywuzzy python-Levenshtein


Pip
###

.. warning::

   Pip can interfere with your system python. Make sure to never run
   pip as root, and only perform local installs.

.. note::

   If you are using pip somewhere behind a firewall, you may need to
   pin pip's servers using
   ``pip install --trusted-host pypi.org --trusted-host pythonhosted.org``

**Fetch the latest version of PyPWA and install locally**

.. code-block:: sh

   git clone --depth=1 https://github.com/JeffersonLab/PyPWA.git
   cd PyPWA
   pip install --local .
