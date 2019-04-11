#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.xz \
    f2c1e86ca0a404ff281631bdc8377638992744b175afb806e25871a24a934e07

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T m4.XXXXXX /mere/sources/m4-1.4.18.tar.xz)
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
