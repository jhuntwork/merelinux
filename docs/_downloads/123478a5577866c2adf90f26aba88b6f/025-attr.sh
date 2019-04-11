#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://download.savannah.gnu.org/releases/attr/attr-2.4.48.tar.gz \
    5ead72b358ec709ed00bbf7a9eaef1654baad937c001c044fe8b74c57f5324e7

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T attr.XXXXXX /mere/sources/attr-2.4.48.tar.gz)
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
