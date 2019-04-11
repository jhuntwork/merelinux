#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/automake/automake-1.16.1.tar.xz \
    5d05bb38a23fd3312b10aea93840feec685bdf4a41146e78882848165d3ae921

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T automake.XXXXXX /mere/sources/automake-1.16.1.tar.xz)
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
