#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-2.8.3.tar.gz \
    9b640b13047182761a99ce3e4f000be9687566e0828b4a72709e9e6a3ef98477

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T libressl.XXXXXX /mere/sources/libressl-2.8.3.tar.gz)
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
