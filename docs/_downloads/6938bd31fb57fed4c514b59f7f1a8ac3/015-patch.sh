#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/patch/patch-2.7.6.tar.xz \
    ac610bda97abe0d9f6b7c963255a11dcb196c25e337c61f94e4778d632f1d8fd

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T patch.XXXXXX /mere/sources/patch-2.7.6.tar.xz)
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
