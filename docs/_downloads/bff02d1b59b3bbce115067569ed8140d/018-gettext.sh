#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/gettext/gettext-0.19.8.1.tar.xz \
    105556dbc5c3fbbc2aa0edb46d22d055748b6f5c7cd7a8d99f8e7eb84e938be4

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T gettext.XXXXXX /mere/sources/gettext-0.19.8.1.tar.xz)
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
