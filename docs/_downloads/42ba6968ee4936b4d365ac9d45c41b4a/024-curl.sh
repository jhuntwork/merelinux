#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://curl.haxx.se/download/curl-7.64.1.tar.bz2 \
    4cc7c738b35250d0680f29e93e0820c4cb40035f43514ea3ec8d60322d41a45d

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T curl.XXXXXX /mere/sources/curl-7.64.1.tar.bz2)
cd "${source_dir:?}"

# Musl uses poll.h instead of sys/poll.h and so multiple warnings will
# be issued throughout the build. Though harmless, it is easy to correct.
grep -lr 'sys/poll.h' . | while read -r file ; do
    sed -i 's@sys/poll.h@poll.h@g' "$file"
done

# Configure the build
PATH_SEPARATOR=':' ./configure --prefix=/mere \
    --with-ca-bundle=/mere/etc/ssl/cert.pem

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
