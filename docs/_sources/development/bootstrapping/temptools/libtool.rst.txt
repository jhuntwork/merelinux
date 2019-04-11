Libtool
=======


.. glossary::

    Description
        A generic library support script.

    Rationale
        Many source packages ship with pre-generated build scripts. Pacman does not. Autoconf, automake and libtool are required to generate them before using.




The following script [#f1]_ outlines the commands required to complete this step:

.. literalinclude:: mere_temptools_scripts/021-libtool.sh
    :language: bash


.. [#f1] :download:`021-libtool.sh <mere_temptools_scripts/021-libtool.sh>`
