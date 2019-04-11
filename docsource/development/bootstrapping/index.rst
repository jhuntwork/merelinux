.. _bootstrapping:

Bootstrapping
=============

Realistically, a packaged distribution only needs to be bootstrapped once.
After that, packages can be easily upgraded individually. However, the process
of starting essentially from nothing and creating a system which can re-build
itself is interesting. At least, it is to me. The
`Linux From Scratch <http://www.linuxfromscratch.org/lfs/>`_ (LFS) project is
an excellent resource for understanding the what, why and how of such an
endeavor. In fact, this bootstrapping process borrows a number of things
from LFS.

So why bother documenting this at all? For a few reasons:

#. There are some differences when building a native
   `musl libc <http://www.musl-libc.org>`_ toolchain compared to the library
   LFS uses,  Glibc.
#. Although the wider LFS community provides a few documents and some tools
   around package management, LFS itself does not really support it. This
   documentation aims to show more fully what it is like to bootstrap a system
   with package management in mind, and specifically,
   `pacman <https://www.archlinux.org/pacman/>`_.
#. When packaging, Mere has adopted a method that does not rely solely on a
   :command:`chroot` environment like LFS, nor a :command:`fakeroot`-based
   setup that pacman's included :command:`makepkg` tool expects. Instead, it
   uses containers via `LXC <https://linuxcontainers.org>`_. One advantage is
   that the environment where the packages are built is more fully isolated.
   Unlike a simple chroot, the container has its own process and network
   namespaces. Therefore it is reasonably safe to compile and package within
   the container as a privileged user. In turn, this removes the need to
   depend on the LD_PRELOAD hackery of :command:`fakeroot`.
   Finally, containers can be easily torn down and recreated through a
   repeatable mechanism. This allows for better control over
   dependencies while at the same time making automation easier.
#. `busybox <https://busybox.net>`_ is very usable as a lightweight
   replacement for the utilities included in the  `bzip2`, `coreutils`,
   `diffutils`, `findutils`, `gawk`, `grep`, `gzip`, `inetutils`,
   `iproute2`, `kbd`, `sed`, `sysklogd`, `tar`, and `util-linux` packages.
   This process demonstrates that. While there are some minor features missing,
   most will likely not be noticed, or are easily worked around.
#. It was fun! I enjoyed documenting everything and perhaps someone else will
   find it useful.

.. toctree::
    :hidden:

    setup_environment
    temptools
    packaging
