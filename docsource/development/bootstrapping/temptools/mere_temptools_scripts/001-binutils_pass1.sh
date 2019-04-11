#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/binutils/binutils-2.32.tar.xz \
    0ab6c55dd86a92ed561972ba15b9b70a8b9f75557f896446c82e8b36e473ee04

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T binutils_pass1.XXXXXX /mere/sources/binutils-2.32.tar.xz)
cd "${source_dir:?}"

# Create an empty directory inside the unpacked source code:
mkdir -v build
cd build

# Configure the build
../configure --prefix=/mere \
    --with-sysroot=/ \
    --with-lib-path=/mere/lib \
    --host=${SYS_REAL} \
    --build=${SYS_REAL} \
    --target=${SYS_FAKE} \
    --disable-nls \
    --disable-werror

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
