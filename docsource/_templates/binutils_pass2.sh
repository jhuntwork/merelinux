{% extends "buildpackage.sh" %}
{% block build %}
# Create an empty directory inside the unpacked source code:
mkdir -v build
cd build

# Configure the build
CC=${SYS_FAKE}-gcc \
    AR=${SYS_FAKE}-ar \
    RANLIB=${SYS_FAKE}-ranlib \
    ../configure --prefix=/mere \
    --with-sysroot \
    --with-lib-path=/mere/lib \
    --build=${SYS_REAL} \
    --host=${SYS_REAL} \
    --target=${SYS_REAL} \
    --disable-nls \
    --disable-werror

# Compile
make

# Install
make install

# Clean the build tree and compile and install a new linker with the final
# lib path for use later
make -C ld clean
make -C ld LIB_PATH=/lib
cp -v ld/ld-new /mere/bin

{% endblock %}
