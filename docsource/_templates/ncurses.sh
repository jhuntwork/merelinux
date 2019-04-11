{% extends "buildpackage.sh" %}
{% block build %}
# Don't use mawk if it happens to be on the host system
sed -i s/mawk// configure

# Configure the build
./configure --prefix=/mere \
    --with-shared \
    --without-debug \
    --without-ada \
    --enable-widec \
    --enable-overwrite

# Compile
make

# Install
make install

{% endblock %}
