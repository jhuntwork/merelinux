{% extends "buildpackage.sh" %}
{% block build %}
# Prepare the headers
make INSTALL_HDR_PATH=dest headers_install

# Install the headers
cp -rv dest/include/* /mere/include

{% endblock %}
