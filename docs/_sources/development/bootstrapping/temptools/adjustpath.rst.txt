Adjust PATH
===========
At this point, :file:`/mere` should contain everything that is needed to
successfully build the rest of the temporary tools. As a further protection
from utilities in the host system being discovered and referenced in
generated scripts, adjust the PATH environment variable to only contain
:file:`/mere/bin`.




The following script [#f1]_ outlines the commands required to complete this step:

.. literalinclude:: mere_temptools_scripts/011-adjustpath.sh
    :language: bash


.. [#f1] :download:`011-adjustpath.sh <mere_temptools_scripts/011-adjustpath.sh>`
