
############
Installation
############

PyPWA can be installed with ``pip`` or ``conda`` with Python 3.7 or newer



Conda
#####

.. note::

   PyPWA works on Macintosh, but we currently do not have a build for it in
   Anaconda's cloud system. This will change soon, please be patient with us.


Thanks to tools provided by Anaconda, you can easily install PyPWA and all
it's dependencies with a simple one line command

.. code-block:: sh

   conda install -c markjonestx pypwa

If you want tools from PWA2000 (GAMP, HGAMP, VAMP, PPGEN) we've included them
as well

.. code-block:: sh

   conda install -c markjonesyx pwa2000

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
