Temporary Tools
===============

.. include:: /_templates/buildorder.rst

Before we can start building actual pacman packages, we need a toolchain that
can compile and link against musl libc, as well as pacman itself. We'll also
compile LXC for more complete control over how containers are created and used
when building final system packages.

LFS provides a lot of details concerning the technical aspects of
`bootstrapping a toolchain
<http://www.linuxfromscratch.org/lfs/view/stable/chapter05/toolchaintechnotes.html>`_,
so I'll refrain from diving too deeply into that
here. However, I will aim to note why certain packages are included and any
points of particular interest.

Each subsection will outline steps to complete through an embedded script. The
goal of presenting the commands in this way was to provide a balance between
readability and automation. Copying and pasting the commands from a browser
should work just fine, however exercise care about pasting multiple commands,
since subsequent commands will execute even if previous ones failed.

If you want to execute the scripts directly, there is a link to download an
individual script as a footnote at the bottom of each section. You can also
download the whole collection of scripts in a single archive. [#f1]_

Each script is numbered according to execution order, so if you download all of
them, or even just a few in order, a simple tool to execute each in order will
provide you with basic automation for the whole temptools section.

Here is a full working example using a Python package:

.. code-block:: bash

   pip install runsteps
   tar -xf mere_temptools_scripts.tar.gz
   runsteps -v mere_temptools_scripts

.. [#f1] :download:`mere_temptools_scripts.tar.gz <temptools/mere_temptools_scripts.tar.gz>`
