#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://download.savannah.gnu.org/releases/acl/acl-2.2.53.tar.gz \
    06be9865c6f418d851ff4494e12406568353b891ffe1f596b34693c387af26c7

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T acl.XXXXXX /mere/sources/acl-2.2.53.tar.gz)
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
