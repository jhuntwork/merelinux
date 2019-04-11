{% extends "buildpackage.sh" %}
{% block build %}
# Create an empty directory inside the unpacked source code:
mkdir -v build
cd build

# Configure the build
../configure --prefix=/mere \
    --with-sysroot=/ \
    --with-lib-path=/mere/lib \
    --host=${SYS_REAL} \
    --build=${SYS_REAL} \
    --target=${SYS_FAKE} \
    --disable-nls \
    --disable-werror

# Compile
make

# Install
make install

{% endblock %}
