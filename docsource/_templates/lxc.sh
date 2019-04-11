{% extends "buildpackage.sh" %}
{% block build %}
# Configure the build
./configure --prefix=/mere \
    --disable-werror \
    --with-init-script=none

# Compile
make

# Install
make install

# Add the template script for creating merebuild containers
install -m0755 /mere/sources/merelinux/packages/lxc/lxc-merebuild \
    /mere/share/lxc/templates/lxc-merebuild

# Add a special hook script to setup /dev/tty inside the container
install -m0755 /mere/sources/merelinux/packages/lxc/autodev.hook.sh \
    /mere/share/lxc/

{% endblock %}
