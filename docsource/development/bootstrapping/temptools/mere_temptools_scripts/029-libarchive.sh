#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://www.libarchive.org/downloads/libarchive-3.3.3.tar.gz \
    ba7eb1781c9fbbae178c4c6bad1c6eb08edab9a1496c64833d1715d022b30e2e

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T libarchive.XXXXXX /mere/sources/libarchive-3.3.3.tar.gz)
cd "${source_dir:?}"

# A minor fix for compatibility with Musl
sed -i 's@HAVE_LCHMOD@&_DISABLE@' libarchive/archive_write_disk_posix.c

# Configure the build
./configure --prefix=/mere

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
