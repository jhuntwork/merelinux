{% extends "buildpackage.sh" %}
{% block build %}
# Overwrite an internal script to use sed instead of ed
install -m0755 /mere/sources/merelinux/packages/bc/fix-libmath_h \
    bc/fix-libmath_h

# Configure the build
./configure --prefix=/mere

# Remove a dependency the build has on texinfo
printf '%s\n' "MAKEINFO = :" >> doc/Makefile

# Compile
make

# Install
make install

{% endblock %}
