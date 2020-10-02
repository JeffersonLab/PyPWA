
############
Installation
############

PyPWA can be installed with ``pip`` or ``conda`` with Python 3.7 or newer



Conda
#####

Thanks to tools provided by Anaconda, you can easily install PyPWA and all
it's dependencies with a simple one line command. Check out `Anaconda's
user guide <https://docs.anaconda.com/anaconda/user-guide/>`_ if you're
new to using Anaconda.

.. code-block:: sh

   conda install -c markjonestx pypwa

If you want tools from PWA2000 (GAMP, HGAMP, VAMP, PPGEN) we've included them
as well

.. note::
    PWA2000 is currently only available on Linux installs of Anaconda.

.. code-block:: sh

   conda install -c markjonesyx pwa2000

Pip
###

.. warning::

   Pip can interfere with your system python. Make sure to never run
   pip as root, and only perform local installs.

**Fetch the latest version of PyPWA and install locally**

.. note::

   If you are using pip somewhere behind a firewall, you may need to
   pin pip's servers using
   ``pip install --trusted-host pypi.org --trusted-host pythonhosted.org``

.. code-block:: sh

   git clone --depth=1 https://github.com/JeffersonLab/PyPWA.git
   cd PyPWA
   pip install --local .
