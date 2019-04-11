#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://zlib.net/zlib-1.2.11.tar.xz \
    4ff941449631ace0d4d203e3483be9dbc9da454084111f97ea0a2114e19bf066

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T zlib.XXXXXX /mere/sources/zlib-1.2.11.tar.xz)
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
