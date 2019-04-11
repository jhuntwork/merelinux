Extra Packages
==============

.. toctree::
   :hidden:

This section will highlight building a few other packages which are not
strictly required, but either demonstrate functionality, or make the system
more comfortable to interact with.

.. note::

    The Disk Image Packages and Demo Packages are considered required in order
    to complete the process in this documentation. The Comfort Packages are
    optional.

Disk Image Packages
-------------------

There are a few packages that are required in order to create a bootable
disk image, but are not strictly necessary at run-time.

E2fsprogs
~~~~~~~~~

Although `busybox` provides some of the tools found in this package,
the ones `e2fsprogs` provides for creating filesystems are preferable.
Also there are two libraries that other packages use: `libblkid`, and
`libuuid`. For example, `syslinux` requires `libuuid`.

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/e2fsprogs -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/e2fsprogs

Syslinux
~~~~~~~~

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/syslinux -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/syslinux

Popt
~~~~

Popt is a command line argument parser that Gptfdisk uses.

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/popt -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/popt

Gptfdisk
~~~~~~~~

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/gptfdisk -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/gptfdisk

Libdevmapper
~~~~~~~~~~~~

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/libdevmapper -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/libdevmapper

Git
~~~

The next package, kpartx, desn't have a release archive, but only
uses git tags for releases, so we need to build git so that Pacman's
:command:`makepkg` can retrieve the source.

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/git -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/git

Kpartx
~~~~~~

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/kpartx -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/kpartx

Demo Packages
-------------

For demo purposes, all we really need is a simple service to run at boot-time
and show that the system is working. `nginx` serves this nicely. It
requires the PCRE library, however, so build that first:

PCRE
~~~~

.. code-block:: bash

      # Build the package
      sudo ./scripts/build.sh packages/pcre -a

      # Add any new packages built to the repo
      sudo ./scripts/add_all_new_pkgs.sh packages/pcre

Nginx
~~~~~

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/nginx -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/nginx

Comfort Packages
----------------

Recall from the :ref:`design-considerations-and-goals` section that one of the
stated goals of Mere is to *run services*, and to do so in a manageable,
scalable fashion. This means that catering to use cases where one manages an
individual servier by logging in, either locally or via ssh, and manipulating
files is an anti-pattern we discourage. By extension, certain packages and
utilities aren't strictly necessary to achieve such a goal.

That being said, when developing or testing it can still be extremely useful
to have a more comfortable environment. So here are a few other packages
which may make the system seem more friendly.

Mksh
~~~~

:command:`mksh` is a more full-featured shell than :command:`sh`, but still
more lightweight than :command:`bash`.

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/mksh -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/mksh

Mandoc
~~~~~~

`mandoc` provides a small man page reader.

.. code-block:: bash

      # Build the package
      sudo ./scripts/build.sh packages/mandoc -a

      # Add any new packages built to the repo
      sudo ./scripts/add_all_new_pkgs.sh packages/mandoc

Dropbear
~~~~~~~~

`dropbear` is a lightweight SSH server.

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/dropbear -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/dropbear

Vim
~~~

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/vim -a

    # Add any new packages built to the repo
    sudo ./scripts/add_all_new_pkgs.sh packages/vim

That's it! That's everything needed to demonstrate the usability of the system.
There are other package recipes included in the merelinux source tree that you
can build or modify if you choose. To see the system in action, head to the
:ref:`create-disk-image` section.
