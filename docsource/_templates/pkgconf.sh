{% extends "buildpackage.sh" %}
{% block build %}
# Configure the build
./autogen.sh
./configure --prefix=/mere

# Compile
make

# Install
make install
ln -s pkgconf /mere/bin/pkg-config

{% endblock %}
