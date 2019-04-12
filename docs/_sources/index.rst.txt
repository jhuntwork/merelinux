Mere Linux
==========

.. toctree::
   :includehidden:
   :hidden:

   gettingstarted/index
   development/index
   concepts/index

Mere Linux is a simple Linux distribution built upon
`musl libc <http://www.musl-libc.org/>`_ and aimed at virtualized or
containerized server instances. It also features
`pacman <https://www.archlinux.org/pacman/>`_ as the package manager and
`s6 <http://skarnet.org/software/s6/>`_ for process supervision and process 1,
or init.

Why Another Distribution?
-------------------------

Really, if we're being honest, the main reason is because it's fun to build.

There are a lot of distributions out there. Many of them have great ideas
and implementations, and most are well suited for a wide variety of purposes.
But its quite enjoyable to piece together your own system, choosing the
elements that fit your specific needs and ideals.

The goal of Mere Linux isn't to achieve widespread adoption. It won't fill a
niche that has never been touched before. The goal is simply to document and
provide an alternative approach. Specifically, the combination of `musl`,
`pacman` and `s6` make for a simple but robust alternative.

Having said that, there are some fundamental principles that have guided how
Mere has been shaped.

.. _design-considerations-and-goals:

Design Considerations and Goals
-------------------------------

* Simplicity over features
* Readability and usability over cleverness
* The primary use case is `Microservices <https://en.wikipedia.org/wiki/Microservices>`_
* `Separation of Concerns <https://en.wikipedia.org/wiki/Separation_of_concerns>`_
  and similarly, the `Unix Philosophy <https://en.wikipedia.org/wiki/Unix_philosophy>`_
* Static binaries where feasible for improved performance and portability
* Immutable Infrastructure

   * Treat the OS as if admins will rarely, if ever, login to a shell
   * `Pets vs. Cattle <https://blog.engineyard.com/2014/pets-vs-cattle>`_
