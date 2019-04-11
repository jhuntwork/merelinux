#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    https://ftp.gnu.org/gnu/nettle/nettle-3.4.1.tar.gz \
    f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T nettle.XXXXXX /mere/sources/nettle-3.4.1.tar.gz)
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
