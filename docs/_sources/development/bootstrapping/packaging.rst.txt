Packaging the Final System
==========================

.. toctree::
   :hidden:
   :numbered:

   packaging/prepare
   packaging/base-layout
   packaging/core
   packaging/extra

All the tools required to use Pacman to package components of the final system
should now be built and installed. We will drop in just a little more
configuration and then walk through building the first package "by hand". Next,
we will use scripts included in the source tree to further automate those
manual steps and one-by-one build out the packages required for a basic
Mere Linux system.

Each package will be built using the Mere Linux build recipe for that
package. These are located in the merelinux source tree, under the directory
`packages`. Every package has its own directory, typically matching the name of
the package, and each directory contains at least a :file:`PKGBUILD` file and a
:file:`ChangeLog` file. There may also be patches for some fixes or additional
configuration files or scripts that will ship with the package for extra
functionality.

.. warning::

    Be advised that changes to core packages may cause the bootstrapping steps
    to fail.

The above warning aside, I encourage you to peruse the contents of any package
and make any changes you wish for your system. The
`PKGBUILD wiki page <https://wiki.archlinux.org/index.php/PKGBUILD>`_ provides
a good starting point for understanding the contents of these recipes.
