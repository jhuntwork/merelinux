#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    https://github.com/pkgconf/pkgconf/archive/pkgconf-1.6.0.tar.gz \
    b4428d70a7f38bd920b6dee617e1c0264afad7a747200715a9a46de9230067c8

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T pkgconf.XXXXXX /mere/sources/pkgconf-1.6.0.tar.gz)
cd "${source_dir:?}"

# Configure the build
./autogen.sh
./configure --prefix=/mere

# Compile
make

# Install
make install
ln -s pkgconf /mere/bin/pkg-config

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
