.. _static-tools:

Static Tools
============

The fastest way to get setup for developing and building Mere Linux packages
is to download and configure static versions of three packages.

First, grab the latest pacman release:

.. code-block:: bash

   curl -LO http://repo.merelinux.org/stable/pacman-latest-x86_64.pkg.tar.xz

Extract the package:

.. code-block:: bash

   TMPDIR=$(mktemp -d)
   tar -C "$TMPDIR" -xf pacman-latest-x86_64.pkg.tar.xz

Using the temporary pacman, install to the `/mere` directory some static copies
of pacman and lxc:

.. code-block:: bash

   sudo install -d /mere/var/lib/pacman /mere/pkgs
   sudo "$TMPDIR/bin/pacman" -Sy --config "$TMPDIR/etc/pacman.conf" \
       -b /mere/var/lib/pacman \
       lxc-portable pacman-portable

Now, using the installed pacman, also install busybox to the `/mere` directory:

.. code-block:: bash

   sudo touch /mere/pkgs/buildlocal.db
   sudo /mere/bin/pacman -Sy -r /mere -b /mere/var/lib/pacman busybox

These operations will have installed new items as the `root` user so change
the contents of `/mere` once again to be owned by your current user:

.. code-block:: bash

   sudo chown -R $(whoami) /mere

Clean up the temporary directory:

.. code-block:: bash

   rm -rf "$TMPDIR"

.. include:: ../_templates/configure_lxc.rst

Great! Now you're ready to start working. Head on over to :ref:`workflow` if
you're looking to build custom packages, or back to :ref:`create-disk-image` if
you're just interested in kicking the tires.
