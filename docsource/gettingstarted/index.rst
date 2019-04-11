Getting Started
===============

The easiest way to start using and investigating Mere Linux is to download and
run the latest Docker image. This of course requires
`docker <https://docs.docker.com/>`_ running on your system. Alternatively, you
can create your own disk image for use in a virtual machine, either locally or
in a cloud environment. And if you are able to successfully create your own
disk image, then you likely have the skills required to run that image on
actual hardware, too.

Docker
------

.. code-block:: bash

   docker run -it mere/base

Once inside the container, use :command:`pacman` to investigate and install new
packages:

.. code-block:: bash

   # Update the local pacman database
   pacman -Sy

   # Query what is installed
   pacman -Q

   # Upgrade existing packages
   pacman -Syu

   # Install a new package, for example, a nicer shell
   pacman -Sy mksh
   exec /bin/mksh -l


.. _create-disk-image:

Creating a Disk Image
---------------------

These steps will create a disk image that can be used in a Virtual Machine,
like VirtualBox, or in a cloud environment like GCE.

.. note::

   These instructions assume you have set up the development tools as
   specified in the :ref:`development` section. If not, please proceed there
   first, and choose one of the two options.

Prepare a Working Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, create an empty, basic merebuild container:

.. code-block:: bash

    sudo /mere/bin/lxc-create -t merebuild -n merebuild-dimage

The :doc:`../development/scripts/disk_image` script will do the heavy lifting
of creating the disk image, so install that to the new container:

.. code-block:: bash

    sudo install -m0755 scripts/disk_image \
        /mere/var/lib/lxc/merebuild-dimage/rootfs/bin/

Next, enter into the container with a login shell:

.. code-block:: bash

    sudo /mere/bin/lxc-start -n merebuild-dimage -F -- \
        /bin/env -i \
        TERM=$TERM \
        http_proxy=${http_proxy} \
        https_proxy=${https_proxy} \
        SHELL=/bin/bash \
        HOME=/root \
        /bin/bash -l

Now, install some required packages:

.. code-block:: bash

    pacman -Sy --noconfirm e2fsprogs syslinux gptfdisk kpartx

Good! Now you're ready to create the disk image, which you'll do inside this
container.

Create the Image
~~~~~~~~~~~~~~~~

First, set a variable to a value of your choice. This will be the root
password of the image you create:

.. code-block:: bash

    export mypass='somekindofpassword'

Optionally, if you want to login over ssh and inspect the system directly,
set a variable that controls the installation of the comfort packages:

.. code-block:: bash

    export comfortable=1

The default disk size used in the following script is 1G. The image can
easily be resized later, after creation, but if you would like a different
size from the start, specify it:

.. code-block:: bash

    export disk_size=10G

Create the image by running the disk_image script:

.. code-block:: bash

    disk_image

And finally compress the image:

.. code-block:: bash

    tar -C /tmp -czf /meredisk.tar.gz disk.raw

.. note::

   The new disk image will be located in the container's root filesystem,
   so after you exit the container, you'll probably want to move it
   somewhere, like:
   `sudo mv /mere/var/lib/lxc/merebuild-dimage/rootfs/meredisk.tar.gz .`

The resulting file can be uploaded to Google Cloud and used as a source
for a custom disk image there as per the instructions at
`<https://cloud.google.com/compute/docs/images/import-existing-image#import_image>`_.
Or if you unpack the tar archive, you can use the VirtualBox tool
:command:`VBoxManage` to convert the `disk.raw` file into a format usable by
VirtualBox and run the system in a virtual machine there. For example:

.. code-block:: bash

    VBoxManage convertdd disk.raw newdisk.vdi --format VDI

Resize the Image
~~~~~~~~~~~~~~~~

If you want to resize the image at any point, take a look at the
:doc:`../development/scripts/resize_disk` script which can also be run inside a
merebuild container.
