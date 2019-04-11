#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    ftp://ftp.astron.com/pub/file/file-5.35.tar.gz \
    30c45e817440779be7aac523a905b123cba2a6ed0bf4f5439e1e99ba940b5546

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T file.XXXXXX /mere/sources/file-5.35.tar.gz)
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
