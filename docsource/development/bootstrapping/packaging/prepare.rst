Prepare for Packaging
=====================

.. toctree::
   :hidden:

The rest of this section will make use of the temporary tools, but does not
require a clean environment or a modified PATH. Also, it is assumed that
all commands are being issued from within the `merelinux` source tree, checked
out earlier via git.

First, set some environment variables which will alter how the merebuild
containers are created. These are important during this phase to allow
bootstrapping to finish successfully.

.. code-block:: bash

    export mere_bootstrap=1
    export mere_base=none

.. include:: ../../../_templates/configure_lxc.rst

Finally, change directories to the `merelinux` source tree. All the rest of
this section assumes the commands are run from there:

.. code-block:: bash

    cd /mere/sources/merelinux
