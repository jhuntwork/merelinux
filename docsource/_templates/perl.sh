{% extends "buildpackage.sh" %}
{% block build %}
# Configure the build
sh Configure -des -Dprefix=/mere -Dlibs=-lm

# Compile
make

# Install
make install

{% endblock %}
