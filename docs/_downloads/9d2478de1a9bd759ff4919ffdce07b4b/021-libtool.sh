#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/libtool/libtool-2.4.6.tar.xz \
    7c87a8c2c8c0fc9cd5019e402bed4292462d00a718a7cd5f11218153bf28b26f

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T libtool.XXXXXX /mere/sources/libtool-2.4.6.tar.xz)
cd "${source_dir:?}"

# Configure the build
./configure --prefix=/mere

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
