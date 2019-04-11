{% extends "buildpackage.sh" %}
{% block build %}
# A minor fix for compatibility with Musl
sed -i 's@HAVE_LCHMOD@&_DISABLE@' libarchive/archive_write_disk_posix.c

# Configure the build
./configure --prefix=/mere

# Compile
make

# Install
make install

{% endblock %}
