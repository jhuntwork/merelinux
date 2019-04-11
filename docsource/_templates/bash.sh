{% extends "buildpackage.sh" %}
{% block build %}
# Configure the build
./configure --prefix=/mere \
    --without-bash-malloc

# Compile
make

# Install
make install

{% endblock %}
