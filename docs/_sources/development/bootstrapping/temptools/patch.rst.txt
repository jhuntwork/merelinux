Patch
=====


.. glossary::

    Description
        A utility for patching difference listings against one or more original files

    Rationale
        The patch utility is expected to be present for full pacman functionality. Busybox ships with a version of patch, but its features are not sufficient for our needs.




The following script [#f1]_ outlines the commands required to complete this step:

.. literalinclude:: mere_temptools_scripts/015-patch.sh
    :language: bash


.. [#f1] :download:`015-patch.sh <mere_temptools_scripts/015-patch.sh>`
