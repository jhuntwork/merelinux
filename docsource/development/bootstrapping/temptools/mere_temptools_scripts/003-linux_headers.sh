#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.19.34.tar.xz \
    dd795e2a1fddbee5b03c3bb55a1926829cc08df4fdcabce62dda717ba087b8cc

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T linux_headers.XXXXXX /mere/sources/linux-4.19.34.tar.xz)
cd "${source_dir:?}"

# Prepare the headers
make INSTALL_HDR_PATH=dest headers_install

# Install the headers
cp -rv dest/include/* /mere/include

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
