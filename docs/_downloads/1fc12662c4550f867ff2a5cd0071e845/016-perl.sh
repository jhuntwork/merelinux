#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://www.cpan.org/src/5.0/perl-5.28.1.tar.xz \
    fea7162d4cca940a387f0587b93f6737d884bf74d8a9d7cfd978bc12cd0b202d

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T perl.XXXXXX /mere/sources/perl-5.28.1.tar.xz)
cd "${source_dir:?}"

# Configure the build
sh Configure -des -Dprefix=/mere -Dlibs=-lm

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
