#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://busybox.net/downloads/busybox-1.30.1.tar.bz2 \
    3d1d04a4dbd34048f4794815a5c48ebb9eb53c5277e09ffffc060323b95dfbdc

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T busybox.XXXXXX /mere/sources/busybox-1.30.1.tar.bz2)
cd "${source_dir:?}"

# Configure the build
make defconfig
sed -i -e '/CONFIG_PREFIX/s@=.*@="/mere"@' \
       -e '/CONFIG_INSTALL_NO_USR/s@^# @@' \
       -e '/CONFIG_INSTALL_NO_USR/s@ is.*@=y@' .config

# Compile
make busybox

# Install
make install

# Remove a symlink to a feature that is not required and
# will cause ugly warnings when the attr and acl packages build
rm /mere/bin/rpm

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
