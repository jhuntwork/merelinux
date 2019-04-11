#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz \
    b4a80f2ac66170b2913efbfb9f2594f1f76c7b1afd11f799e22035d63077fb4d

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T bash.XXXXXX /mere/sources/bash-5.0.tar.gz)
cd "${source_dir:?}"

# Configure the build
./configure --prefix=/mere \
    --without-bash-malloc

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
