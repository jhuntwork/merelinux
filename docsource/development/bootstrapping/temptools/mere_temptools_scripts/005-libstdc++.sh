#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/gcc/gcc-8.3.0/gcc-8.3.0.tar.xz \
    64baadfe6cc0f4947a84cb12d7f0dfaf45bb58b7e92461639596c21e02d97d2c

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T libstdc++.XXXXXX /mere/sources/gcc-8.3.0.tar.xz)
cd "${source_dir:?}"

# Create an empty directory inside the unpacked source code:
mkdir -v build
cd build

# Configure the build
CFLAGS='-fPIC' \
    CXXFLAGS="-fPIC" \
    CC=${SYS_FAKE}-gcc \
    CXX=${SYS_FAKE}-g++ \
    AR=${SYS_FAKE}-ar \
    RANLIB=${SYS_FAKE}-ranlib \
    ../libstdc++-v3/configure --prefix=/mere \
    --build=${SYS_REAL} \
    --host=${SYS_FAKE} \
    --target=${SYS_REAL} \
    --disable-shared \
    --disable-multilib \
    --disable-nls \
    --disable-libstdcxx-threads \
    --disable-libstdcxx-pch \
    --with-gxx-include-dir=/mere/${SYS_FAKE}/include/c++/8.3.0

# Compile
make

# Install
make install

# Perform another sanity check to ensure libstdc++ is working
echo 'int main(){return 0;}' | ${SYS_FAKE}-g++ -x c++ - -v -lrt -Wl,--verbose | tee output
grep '/mere.*c++.*succeeded' output
readelf -l a.out | grep /mere

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
