#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    https://linuxcontainers.org/downloads/lxc/lxc-2.1.1.tar.gz \
    68663a67450a8d6734e137eac54cc7077209fb15c456eec401a2c26e6386eff6

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T lxc.XXXXXX /mere/sources/lxc-2.1.1.tar.gz)
cd "${source_dir:?}"

# Configure the build
./configure --prefix=/mere \
    --disable-werror \
    --with-init-script=none

# Compile
make

# Install
make install

# Add the template script for creating merebuild containers
install -m0755 /mere/sources/merelinux/packages/lxc/lxc-merebuild \
    /mere/share/lxc/templates/lxc-merebuild

# Add a special hook script to setup /dev/tty inside the container
install -m0755 /mere/sources/merelinux/packages/lxc/autodev.hook.sh \
    /mere/share/lxc/

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
