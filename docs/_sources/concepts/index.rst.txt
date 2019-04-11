Concepts
========

Here we'll explain concepts specific to Mere Linux.

s6
--

The `s6 website <http://skarnet.org/software/s6/>`_ has a great deal of
information explaining what `s6` is, why it came to be, design
objectives and technical guidance around how to use it. So instead of trying to
discuss all of that here, this section will focus on how it is implemented in
Mere.

It would be correct to say that `s6` is the init system of Mere and acts
as the special PID 1. It's more correct to say that `s6` is PID 1 when
Mere is running as a traditional system and not in a container (it's possible
to use `s6` as PID 1 in a container but that's another discussion), and
that :command:`s6-svscan` is PID 1 after `/sbin/init` does some initial setup
at boot-time.

If you were to inspect the contents of `/sbin/init` you would see that it is an
`execline <http://skarnet.org/software/execline/>`_ script that mounts some
important virtual file systems like `/proc` and `/sys` as well as a few other
important things. Lastly it launches `/etc/s6/rc.init` in the background which
makes sure all services configured to start at boot have those configurations
copied to `/s6/run`. Finally, `/sbin/init` execs :command:`s6-svscan` which
monitors `/s6/run` and launches processes to supervise configured services.

The special directory `/s6/run` was chosen instead of the typical `/run`
so that the `s6` package which is statically built could be used
side-by-side with other init processes, for example, if you want to use
`s6` to supervise a process on a non Mere host.

Configured services live in `/etc/s6/services/available` and are enabled to
launch at boot by creating a corresponding symlink in
`/etc/s6/services/enabled`.

Here's what an example service looks like:

.. code-block:: bash

   $ cat /etc/s6/services/enabled/ntpd/run
   #!/bin/execlineb -P
   fdmove -c 2 1
   /sbin/ntpd -dn

:command:`s6-svscan` will launch a :command:`s6-supervise` process that will
continue to respawn the above script if it should die. Therefore, good service
scripts will keep the main process running in the foreground.

Each service can also have its own dedicated, supervised logging process.
Here's an example:

.. code-block:: bash

   $ cat /etc/s6/services/enabled/ntpd/log/run
   #!/bin/execlineb -P
   s6-log -b -- t /var/log/ntpd

This will add logs to `/var/log/ntpd` for this service which are maintained and
rotated throughout the life of the service.

In order to make managing these services a little more friendly and convenient
a :command:`service` script has been written to interact with these components.

Here's a few examples of :command:`service` in use:

.. code-block:: bash

   $ sudo service list

   Service            Status              OnBoot
   ~~~~~~~            ~~~~~~~~            ~~~~~~~~
   dropbear           up                  enabled
   klogd              up                  enabled
   nginx              up                  enabled
   ntpd               up                  enabled
   syslogd            up                  enabled

   $ sudo service klogd disable
   Disabling klogd from launching at boot... OK

   $ sudo service list

   Service            Status              OnBoot
   ~~~~~~~            ~~~~~~~~            ~~~~~~~~
   dropbear           up                  enabled
   klogd              up                  disabled
   nginx              up                  enabled
   ntpd               up                  enabled
   syslogd            up                  enabled

   $ ls -l /etc/s6/services/enabled/klogd
   ls: /etc/s6/services/enabled/klogd: No such file or directory

   $ sudo service klogd status
   up (pid 168) 3508103 seconds

   $ pgrep klogd
   168

   $ sudo service klogd stop
   Stopping klogd... OK

   $ sudo service klogd status
   down (signal 15) 6 seconds, normally up, ready 6 seconds

   $ pgrep klogd

   $ sudo service list

   Service            Status              OnBoot
   ~~~~~~~            ~~~~~~~~            ~~~~~~~~
   dropbear           up                  enabled
   klogd              down                disabled
   nginx              up                  enabled
   ntpd               up                  enabled
   syslogd            up                  enabled

   $ sudo service klogd enable
   Enabling klogd to launch at boot... OK

   $ file /etc/s6/services/enabled/klogd
   /etc/s6/services/enabled/klogd: symbolic link to ../available/klogd

   $ sudo service list

   Service            Status              OnBoot
   ~~~~~~~            ~~~~~~~~            ~~~~~~~~
   dropbear           up                  enabled
   klogd              unknown             enabled
   nginx              up                  enabled
   ntpd               up                  enabled
   syslogd            up                  enabled

   $ sudo service klogd start
   Starting klogd... OK

   $ sudo service list

   Service            Status              OnBoot
   ~~~~~~~            ~~~~~~~~            ~~~~~~~~
   dropbear           up                  enabled
   klogd              up                  enabled
   nginx              up                  enabled
   ntpd               up                  enabled
   syslogd            up                  enabled

   $ sudo service klogd status
   up (pid 3921) 44 seconds

   $ pgrep klogd
   3921


