{% extends "buildpackage.sh" %}
{% block build %}
# Compile and Install
make RAISE_SETFCAP=no prefix=/mere lib=lib install

{% endblock %}
