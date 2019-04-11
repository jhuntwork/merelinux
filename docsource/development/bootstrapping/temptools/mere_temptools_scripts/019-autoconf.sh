#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.xz \
    64ebcec9f8ac5b2487125a86a7760d2591ac9e1d3dbd59489633f9de62a57684

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T autoconf.XXXXXX /mere/sources/autoconf-2.69.tar.xz)
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
