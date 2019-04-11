Configure LXC
-------------

The merebuild containers need network access for downloading resources. The
simplest way to consistently accomplish this is to add a bridge interface on
the host and an iptables rule that allows NAT forwarding.

To set this up, create the following script:

.. code-block:: bash

    cat >preplxc << "EOF"
    #/bin/sh -e
    /mere/sbin/brctl addbr mere0 2>/dev/null || true
    /mere/sbin/brctl setfd mere0 0
    /mere/sbin/ifconfig mere0 10.10.10.1 netmask 255.255.255.0 promisc up
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    echo 1 >/proc/sys/net/ipv4/ip_forward

    mountpoint -q /sys/fs/cgroup || mount -t tmpfs cgroupfs /sys/fs/cgroup
    awk '!/^#/ { if ($4 == 1) print $1 }' /proc/cgroups | \
            while IFS= read -r sys; do
        sys_path="/sys/fs/cgroup/${sys}"
        mkdir -p "$sys_path"
        mountpoint -q "$sys_path" ||
            mount -n -t cgroup -o "$sys" cgroup "$sys_path" ||
            rmdir "$sys_path" ||
            true
    done
    EOF
    sudo install -m0754 preplxc /mere/bin/preplxc

.. note::

    The above script assumes 'eth0' is the name of the interface used for
    accessing the internet. If a different device is used, substitute with the
    correct name on the `iptables` line.


And of course, to execute it, run:

.. code-block:: bash

    sudo /mere/bin/preplxc

.. note::

    The changes this script makes will not survive a reboot. If you want them
    to be persistent, refer to the documentation of your host OS. An example
    for Debian-based systems is here: `<https://wiki.debian.org/LXC/SimpleBridge>`_.

Assuming the above networking configuration is used, the following default
configuration will give the containers access to the network as well as
read-only access to important packaging directories. If you used different
adpater names or IP addresses, you will need to make the corresponding changes
below.

.. code-block:: bash

    printf '
    # Basic settings
    lxc.uts.name = merebuild-container

    # Network settings
    lxc.net.0.type = veth
    lxc.net.0.flags = up
    lxc.net.0.link = mere0
    lxc.net.0.ipv4.address = 10.10.10.10/24
    lxc.net.0.ipv4.gateway = 10.10.10.1

    # Kernel/Virtual Mount Entries
    lxc.autodev = 1
    lxc.hook.autodev = /mere/share/lxc/autodev.hook.sh
    lxc.mount.auto = proc:mixed sys:ro
    lxc.mount.entry = shm dev/shm tmpfs rw,nosuid,nodev,noexec,relatime,mode=1777,size=256m,create=dir 0 0

    # Mere-specific Mount Entries
    lxc.mount.entry = /mere mere none defaults,bind 0 0
    ' | sudo tee /mere/etc/lxc/default.conf
