Setup a Default Environment
===========================

.. toctree::
   :hidden:

Building a self-contained toolchain within another running system requires a
lot of specific configuration. Here we will set up some default directories
and install a few helper scripts.

Link a couple of utilities to the host's copies for now. They will be replaced
later.

.. code-block:: bash

    ln -s /bin/bash /mere/bin/bash
    ln -s $(command -v curl) /mere/bin/curl

Helper Scripts
--------------

The rest of this section assumes the following scripts are installed for the
sake of consistency and ease of automation:

.. glossary::

    :doc:`../scripts/clean_env`
        A script intended to be sourced which allows each build script to
        start with a clean environment

    :doc:`../scripts/fetch`
        A helper tool for downloading resources and verifying its content
        matches expectations

    :doc:`../scripts/unpack`
        A helper tool for consistently unpacking archives and dynamically
        discovering the top-level directory of the extracted archive

Install them:

.. code-block:: bash

    install -m0755 /mere/sources/merelinux/scripts/clean_env  /mere/bin/
    install -m0755 /mere/sources/merelinux/scripts/fetch      /mere/bin/
    install -m0755 /mere/sources/merelinux/scripts/unpack     /mere/bin/
