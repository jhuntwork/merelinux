{% extends "buildpackage.sh" %}
{% block build %}
# Musl uses poll.h instead of sys/poll.h and so multiple warnings will
# be issued throughout the build. Though harmless, it is easy to correct.
grep -lr 'sys/poll.h' . | while read -r file ; do
    sed -i 's@sys/poll.h@poll.h@g' "$file"
done

# Configure the build
PATH_SEPARATOR=':' ./configure --prefix=/mere \
    --with-ca-bundle=/mere/etc/ssl/cert.pem

# Compile
make

# Install
make install

{% endblock %}
