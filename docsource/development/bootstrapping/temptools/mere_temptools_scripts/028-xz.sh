#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://tukaani.org/xz/xz-5.2.4.tar.xz \
    9717ae363760dedf573dad241420c5fea86256b65bc21d2cf71b2b12f0544f4b

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T xz.XXXXXX /mere/sources/xz-5.2.4.tar.xz)
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
