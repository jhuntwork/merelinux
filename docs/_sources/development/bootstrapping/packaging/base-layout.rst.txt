Base Layout
===========

.. toctree::
   :hidden:

Let's build our first package! The base-layout package is really just basic
directory structure for a Mere Linux system. It also includes a few core files
such as a basic :file:`/etc/passwd` file.

.. note::
    One notable difference in Mere from typical Linux systems is the lack of a
    `/usr` directory. Well, actually, there is one, but it is only used for
    compatibility. `/usr` itself is read-only and there are symbolic links for
    crucial sub-directories. For example, `/usr/bin` points to `/bin`. If this
    is not what you want, feel free to change the build instructions located in
    `packages/base-layout/PKGBUILD`. Note however, that you will also most
    likely need to change other critical packages, like gcc to use a more
    typical prefix, like `/usr`.

For this first package, we'll run through some of the steps in a more manual
fashion. But subsequent instructions will advise using a script in the
`scripts` directory that makes building packages a little easier.

First, create the merebuild container where the package will be built. As part
of the creation, :command:`lxc-create` will run through the template installed
in the last section, :file:`/mere/share/lxc/templates/lxc-merebuild`, in case
you'd like to visually inspect it to see what it does:

.. code-block:: bash

    mere_package=packages/base-layout \
        sudo -E /mere/bin/lxc-create -t merebuild -n merebuild-base-layout

.. note::

    The '-E' flag passed to sudo is important to preserve the environment
    variables set in the previous page.

Now, to build the base-layout package, run the following:

.. code-block:: bash

    sudo -E /mere/bin/lxc-start -n merebuild-base-layout -F -- /bin/env -i TERM=$TERM \
        http_proxy=${http_proxy} \
        https_proxy=${https_proxy} \
        HOME=/tmp/wd /bin/sh -lc \
        "cd /tmp/wd && makepkg -fLs --noconfirm"

At this point, it is probably good to give a little helpful info. The root
filesystem for the container will always be in
`/mere/var/lib/lxc/[container-name]/rootfs`.
Inside the container root, the `/tmp/wd` directory is used as a working
directory while building the package. When finished, pacman's `makepkg`
will place any newly created package files in the container's `/tmp/staging`
directory. If all went well, you should see a new file there now:

.. code-block:: bash

    sudo find /mere/var/lib/lxc/merebuild-base-layout/rootfs/tmp/staging

.. note::

    Using `sudo` above is required because the `rootfs` directory is owned
    by the root user and is read only.

Assuming there is a file there named something like
:file:`base-layout-*-x86_64.pkg.tar.xz`, it's time to create a local package
repository and add the new file to it:

.. code-block:: bash

    # Copy over the package file
    sudo find /mere/var/lib/lxc/merebuild-base-layout/rootfs/tmp/staging \
        -name "*.pkg.tar.xz" -exec cp -v '{}' /mere/pkgs \;

    # Add it to the repo
    sudo PATH=/mere/bin:$PATH /mere/bin/repo-add \
        /mere/pkgs/buildlocal.db.tar.gz \
        /mere/pkgs/base-layout-*-x86_64.pkg.tar.xz

Great! The first package has been built and added to the repository.

Let's destroy the container now, which will also remove the container's root
file system. Each step will use fresh containers, created using the packages
that were previously built. Doing this ensures there are no issues with the
packages, it tightly controls the environment in which the packages are built,
and it generally keeps things clean and repeatable.

.. code-block:: bash

    sudo /mere/bin/lxc-destroy -n merebuild-base-layout

Now make sure that the new package is part of the core set of packages which
will be installed when creating new containers:

.. code-block:: bash

    export mere_base=base-layout

There were a lot of commands executed here to create just one simple package.
Doing this over and over for various packages will get tiresome quickly. The
next section will use scripts to automate much of the above for all of the rest
of the core packages.
