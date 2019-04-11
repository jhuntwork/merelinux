#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/ncurses/ncurses-6.1.tar.gz \
    aa057eeeb4a14d470101eff4597d5833dcef5965331be3528c08d99cebaa0d17

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T ncurses.XXXXXX /mere/sources/ncurses-6.1.tar.gz)
cd "${source_dir:?}"

# Don't use mawk if it happens to be on the host system
sed -i s/mawk// configure

# Configure the build
./configure --prefix=/mere \
    --with-shared \
    --without-debug \
    --without-ada \
    --enable-widec \
    --enable-overwrite

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
