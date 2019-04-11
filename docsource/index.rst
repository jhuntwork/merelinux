Mere Linux
==========

.. toctree::
   :includehidden:
   :hidden:

   gettingstarted/index
   development/index
   concepts/index

Mere Linux is a simple Linux distribution built upon `musl libc <http://www.musl-libc.org/>`_
and aimed at virtualized or containerized server instances. It also
features `pacman <https://www.archlinux.org/pacman/>`_ as the package manager
and `s6 <http://skarnet.org/software/s6/>`_ for process supervision and process
1, or init.

Why Another Distribution?
-------------------------

Mainstream Linux distributions have historically been produced with a goal of
covering of two main use cases:

1. A long-lived Web/Internet server, running on physical hardware, supporting
   many users, often managed directly
2. Full-featured desktop systems

As cloud infrastructure continues to gain popularity, such distributions have
often been made to work inside virtual machines and containers, although they
haven’t really been designed for that purpose.

What happens when support for the above use cases are stripped away? What is
the shape and feel of a distribution designed to run *a service*, particularly
where:

* Scalability and flexibility are more important than traditional conventions
* It is understood that administration is not best done individually and directly
* Metrics and logs are intended to be collected and exported externally
* Deployment and configuration happens through instance creation and deletion

Mere Linux aims to find the answer.


.. _design-considerations-and-goals:

Design Considerations and Goals
-------------------------------

Simplicity is often considered a sign of good design and efficiency in purpose.
Mainstream Linux distributions seem to have a hard time keeping things simple
these days, presumably as a result of attempting to cover every conceivable use
case. In contrast, Mere Linux aims to provide a small, simple OS layer for the
purpose of running a single stable web service or application. Below are some
of the technical design patterns which feed and drive a small, simple operating
system.

* `Microservices <https://en.wikipedia.org/wiki/Microservices>`_
* `Continuous Delivery <https://en.wikipedia.org/wiki/Continuous_delivery>`_
* `Separation of Concerns <https://en.wikipedia.org/wiki/Separation_of_concerns>`_
* `Pets vs. Cattle <https://blog.engineyard.com/2014/pets-vs-cattle>`_
* Virtualization and/or Containerization are the primary means of delivering on
  the above today and so become the presumed environment.

Of course, it is possible to adhere to the above principles using one of the
mainstream Linux distributions, but there are often many challenges. What
happens when the OS layer itself is crafted from the beginning to fit these
principles?

Implementation
~~~~~~~~~~~~~~

Here are some of the specific design choices, patterned after the above
principles that have been made so far. (Some may be subject to change as Mere
Linux matures.)

* Use musl libc instead of glibc
* Use pacman for package management
* Replace many common Linux packages with busybox
* Use s6 as init and for supervising services
* Build and ship static binaries, where possible
* Treat the OS as if admins will rarely, if ever, log in to a shell. This has
  implications:

  * While a modest collection of man pages are extremely useful, the need for
    extensive documentation packaged within the running system is reduced.
  * A full featured shell like bash or zsh is not required (pacman build utilities
    currently require bash, but most run-time use cases will not). mksh is
    provided as lightweight, feature-rich, comfortable shell.
* X11, or any desktop support is out of scope
