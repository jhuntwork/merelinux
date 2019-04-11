{% extends "buildpackage.sh" %}
{% block build %}
# Configure the build
make defconfig
sed -i -e '/CONFIG_PREFIX/s@=.*@="/mere"@' \
       -e '/CONFIG_INSTALL_NO_USR/s@^# @@' \
       -e '/CONFIG_INSTALL_NO_USR/s@ is.*@=y@' .config

# Compile
make busybox

# Install
make install

# Remove a symlink to a feature that is not required and
# will cause ugly warnings when the attr and acl packages build
rm /mere/bin/rpm

{% endblock %}
