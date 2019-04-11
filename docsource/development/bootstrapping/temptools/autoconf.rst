Autoconf
========


.. glossary::

    Description
        A tool that produces shell scripts to automatically configure source code.

    Rationale
        Many source packages ship with pre-generated build scripts. Pacman does not. Autoconf, automake and libtool are required to generate them before using.




The following script [#f1]_ outlines the commands required to complete this step:

.. literalinclude:: mere_temptools_scripts/019-autoconf.sh
    :language: bash


.. [#f1] :download:`019-autoconf.sh <mere_temptools_scripts/019-autoconf.sh>`
