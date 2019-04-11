#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/make/make-4.2.1.tar.bz2 \
    d6e262bf3601b42d2b1e4ef8310029e1dcf20083c5446b4b7aa67081fdffc589

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T make.XXXXXX /mere/sources/make-4.2.1.tar.bz2)
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
