Build Essential and Core Packages
=================================

.. toctree::
   :hidden:

In addition to `base-layout`, the core group of packages for any Mere
system is really only `Linux`, `pacman`, `busybox`, and
`s6`. That's all that is required at run-time for a system that boots,
can configure a network connection, has a shell with utilities, can launch
and supervise services, and can install other packages as needed.

In order to have an environment that can *build* packages for Mere, however,
there are several more essential packages required. This section will fill
out all the rest of the packages needed for building, getting most of the
core packages in the process. It will finish by building any remaining core
packages.

.. warning::

    The commands for building when using the included scripts are fairly simple
    and repetitive, but watch out for subtle differences! The process of
    bootstrapping some early packages requires a few special steps.

Linux Headers
-------------

We need the Linux kernel headers now, which are typically packaged alongside
the kernel itself. Because building the kernel would bring in some dependencies
that aren't built yet, we'll use some special features of :command:`makepkg` to
only extract the source and 'repackage' just the headers, without building.
We'll build the full kernel a little bit later on.

.. code-block:: bash

    # Use the build script to enter into the container
    sudo -E ./scripts/build.sh packages/linux

    # Inside the container environment download and extract the source
    makepkg -L -o --nodeps

    # Using a special PKGBUILD file, create only the headers package for now
    makepkg -R -p PKGBUILD-headers --nodeps

    # Exit the container
    exit

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/linux

    # Update the list of required packages:
    export mere_base+=" linux-headers"

The build order of the packages below removes the need to set the variable
in most cases. However there will still be one or two places where it is
required.

Musl
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/musl -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/musl

    # Update the list of required packages:
    export mere_base+=" musl musl-dev"

Adjust the Toolchain
--------------------

Now, adjust the toolchain located in `/mere` to use the paths
provided by the new package:

.. code-block:: bash

    # Move the previously prepared linkers into place
    sudo mv -v /mere/bin/{ld,ld-old}
    sudo mv -v /mere/x86_64-pc-linux-musl/bin/{ld,ld-old}
    sudo mv -v /mere/bin/{ld-new,ld}
    sudo ln -sv /mere/bin/ld /mere/x86_64-pc-linux-musl/bin/ld

    # Adjust gcc's search paths
    /mere/bin/gcc -dumpspecs | sed -e 's@/mere@@g' \
        -e '/\*startfile_prefix_spec:/{n;s@.*@/lib/ @}' \
        -e '/\*cpp:/{n;s@$@ -isystem /include@}' \
        | sudo tee $(dirname $(/mere/bin/gcc --print-libgcc-file-name))/specs

Zlib
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/zlib -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/zlib

Binutils
--------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/binutils -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/binutils

    # Update the list of required packages:
    export mere_base+=" binutils"

GMP
---

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/gmp -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/gmp

MPFR
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/mpfr -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/mpfr

MPC
---

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/mpc -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/mpc

GCC
---

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/gcc -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/gcc

    # Update the list of required packages:
    export mere_base+=" gcc"

Busybox
-------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/busybox -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/busybox

    # Update the list of required packages:
    export mere_base+=" busybox"

M4
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/m4 -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/m4

Gettext
-------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/gettext -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/gettext

Perl
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/perl -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/perl

Autoconf
--------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/autoconf -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/autoconf

Automake
--------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/automake -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/automake

Libtool
-------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/libtool -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/libtool

Ncurses
-------

.. code-block:: bash

    # Build the package
    mere_no_deps=1 sudo -E ./scripts/build.sh packages/ncurses -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/ncurses

The :envvar:`mere_no_deps` variable is used here to tell :command:`makepkg` to
not try to install any missing build dependencies defined in the build recipe.
More specifically, the variable tells :file:`scripts/build.sh` to pass the
:samp:`-d`, or :samp:`--nodeps` flag to :command:`makepkg`.

We do this because `ncurses` requires utilities it itself provides in
order to fully build. Under normal circumstances :command:`makepkg` can just
install the previously built `ncurses` package in the `pacman`
repository. When bootstrapping, however, that's unavailable. Instead we tell it
to ignore dependencies, and the build recipe will just make use of the
utilities already installed in `/mere`.

Readline
--------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/readline -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/readline

Bash
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/bash -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/bash

    # Update the list of required packages:
    export mere_base+=" bash"

Pkgconf
-------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/pkgconf -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/pkgconf

    # Update the list of required packages:
    export mere_base+=" pkgconf"

Make
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/make -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/make

    # Update the list of required packages:
    export mere_base+=" make"

Patch
-----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/patch -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/patch

    # Update the list of required packages:
    export mere_base+=" patch"

Attr
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/attr -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/attr

Acl
---

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/acl -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/acl

Xz
--

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/xz -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/xz

Nettle
------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/nettle -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/nettle

Libarchive
----------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/libarchive -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/libarchive

Libressl
--------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/libressl -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/libressl

Curl
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/curl -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/curl

File
----

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/file -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/file

Pacman
------

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/pacman -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/pacman

Build Essential
---------------

`build-essential` is a meta package that has dependencies on the bare minimum
of packages needed to compile most other packages. When the :envvar:`mere_base`
variable is unset, this package as well as `base-layout` are installed into
new merebuild containers.

.. code-block:: bash

    # Build the package
    sudo -E ./scripts/build.sh packages/build-essential -a

    # Add all new packages to the repository
    sudo -E ./scripts/add_all_new_pkgs.sh packages/build-essential

At this point, we no longer need the extra logic enabled by the environment
variables. Also, all the commands to build a package going forward will
follow the exact same patterns, using the provided scripts.

.. code-block:: bash

    # Unset the environment variables
    unset mere_bootstrap
    unset mere_base

.. note::

   Congragtulations! With the build-essential meta package and all of its
   dependencies built, you have now bootstrapped everything you need to build
   and test your own packages. If that is what you are interested in doing,
   you may want to jump ahead to :ref:`workflow`. Otherwise, continuing here
   will fill out what you need to finish :ref:`create-disk-image`.

There's just two more core items, `linux` and `s6` and their
dependencies remaining to be packaged. Build them now:

Bison
-----

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/bison -a

    # Add all new packages to the repository
    sudo ./scripts/add_all_new_pkgs.sh packages/bison

Flex
----

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/flex -a

    # Add all new packages to the repository
    sudo ./scripts/add_all_new_pkgs.sh packages/flex

Linux
-----

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/linux -a

    # Add all new packages to the repository
    sudo ./scripts/add_all_new_pkgs.sh packages/linux

Skalibs
-------

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/skalibs -a

    # Add all new packages to the repository
    sudo ./scripts/add_all_new_pkgs.sh packages/skalibs

Execline
--------

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/execline -a

    # Add all new packages to the repository
    sudo ./scripts/add_all_new_pkgs.sh packages/execline

S6
--

.. code-block:: bash

    # Build the package
    sudo ./scripts/build.sh packages/s6 -a

    # Add all new packages to the repository
    sudo ./scripts/add_all_new_pkgs.sh packages/s6

Great! At this point the core of the system is built and you have the run-time
packages required for a minimally functional system. It doesn't really do much
though. In the next section we'll add a couple of packages to demonstrate more
useful functionality, and prepare to create a bootable disk image.
