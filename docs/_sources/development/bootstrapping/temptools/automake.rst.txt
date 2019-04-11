Automake
========


.. glossary::

    Description
        A tool for automatically generating Makefile.in files.

    Rationale
        Many source packages ship with pre-generated build scripts. Pacman does not. Autoconf, automake and libtool are required to generate them before using.




The following script [#f1]_ outlines the commands required to complete this step:

.. literalinclude:: mere_temptools_scripts/020-automake.sh
    :language: bash


.. [#f1] :download:`020-automake.sh <mere_temptools_scripts/020-automake.sh>`
