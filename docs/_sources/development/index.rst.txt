.. _development:

Development
===========

To set up a development environment there are currently two choices:
downloading and installing pre-built :ref:`static-tools`, or
:ref:`bootstrapping` your own set of tools using the provided instructions and
scripts as a guide.

Downloading the static tools is certainly easier and faster, but bootstrapping
is arguably more fun. The first option takes at most a few minutes, possibly
seconds, while the second option is at least 2 hours, probably more depending
on how much you do by hand, how fast your hardware is, and how much coffee is
available.

.. warning::

   The Mere Linux build mechanism uses LXC containers, but does not yet support
   unprivileged containers. Perhaps someday it will. In the meantime it is
   recommended that your host development system is one where using privileged
   containers is an acceptable risk.

To get started, you'll need a modern Linux system where the kernel supports
cgroups. Most systems these days do. The instructions here have been tested
using Ubuntu 14.04, though certainly others should work as well. Be sure that
the system has the following utilities installed:

* curl
* git
* iptables
* sudo

The :ref:`bootstrapping` section requires these additional tools:

* bash
* gcc
* make

Start by setting up some important directories:

.. code-block:: bash

    sudo install -d /mere/bin /mere/logs /mere/pkgs /mere/sources

.. glossary::

    `/mere`
        A top-level directory to house everything related to building and
        packaging the final system

    `/mere/bin`
        Houses development scripts and utilities

    `/mere/logs`
        All of the logs pacman creates during packaging will go here

    `/mere/pkgs`
        Stores final system packages and a local pacman repository

    `/mere/sources`
        Downloaded source cache


Now grant your current user ownership of the `/mere` directory and its
contents:

.. code-block:: bash

    sudo chown -R $(whoami) /mere

Finally, clone the Mere Linux repository which contains scripts and build
recipes for the final system packages:

.. code-block:: bash

    cd /mere/sources
    git clone https://github.com/jhuntwork/merelinux

Now it's time to choose your own adventure: :ref:`static-tools`, or
:ref:`bootstrapping`.

.. toctree::
   :hidden:

   static_tools
   bootstrapping/index
   workflow
   scripts
