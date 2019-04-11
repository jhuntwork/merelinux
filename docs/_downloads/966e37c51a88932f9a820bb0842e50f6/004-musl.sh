#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://www.etalabs.net/musl/releases/musl-1.1.22.tar.gz \
    8b0941a48d2f980fd7036cfbd24aa1d414f03d9a0652ecbd5ec5c7ff1bee29e3

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T musl.XXXXXX /mere/sources/musl-1.1.22.tar.gz)
cd "${source_dir:?}"

# Configure the build
./configure --prefix=/mere \
    --syslibdir=/mere/lib \
    --target=${SYS_FAKE}

# Compile
make

# Install
make install

# Install a configuration file which tells the dynamic loader to search
# for libraries in the non-standard path of `/mere/lib`
install -d /mere/etc
echo '/mere/lib' >/mere/etc/ld-musl-x86_64.path

# Perform a quick sanity check to ensure the new libc is being used
echo 'int main(){return 0;}' | ${SYS_FAKE}-gcc -x c - -v -lrt -Wl,--verbose
readelf -l a.out | grep /mere

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
