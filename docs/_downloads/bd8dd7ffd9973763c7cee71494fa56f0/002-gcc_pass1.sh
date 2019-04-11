#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    http://ftp.gnu.org/gnu/gcc/gcc-8.3.0/gcc-8.3.0.tar.xz \
    64baadfe6cc0f4947a84cb12d7f0dfaf45bb58b7e92461639596c21e02d97d2c
fetch \
    https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz \
    87b565e89a9a684fe4ebeeddb8399dce2599f9c9049854ca8c0dfbdea0e21912
fetch \
    http://www.mpfr.org/mpfr-4.0.2/mpfr-4.0.2.tar.xz \
    1d3be708604eae0e42d578ba93b390c2a145f17743a744d8f3f8c2ad5855a38a
fetch \
    http://ftp.gnu.org/gnu/mpc/mpc-1.1.0.tar.gz \
    6985c538143c1208dcb1ac42cedad6ff52e267b47e5f970183a3e75125b43c2e

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T gcc_pass1.XXXXXX /mere/sources/gcc-8.3.0.tar.xz)
cd "${source_dir:?}"

# Unpack the other libraries which will be included in this build:
source_dir_gmp=$(unpack /mere/sources/gmp-6.1.2.tar.xz)
mv "${source_dir_gmp:?}" gmp

source_dir_mpfr=$(unpack /mere/sources/mpfr-4.0.2.tar.xz)
mv "${source_dir_mpfr:?}" mpfr

source_dir_mpc=$(unpack /mere/sources/mpc-1.1.0.tar.gz)
mv "${source_dir_mpc:?}" mpc

# Adjust some of the included configuration files to point at the isolated
# locations in /mere
sed -i 's@/lib\(64\)\?\(32\)\?/ld@/mere&@g' gcc/config/i386/linux64.h
echo '
#undef STANDARD_STARTFILE_PREFIX_1
#undef STANDARD_STARTFILE_PREFIX_2
#define STANDARD_STARTFILE_PREFIX_1 "/mere/lib/"
#define STANDARD_STARTFILE_PREFIX_2 ""' >>gcc/config/i386/linux64.h

# Don't use a lib64 directory
sed -i '/^MULTILIB_OSDIRNAMES/s/lib64/lib/' gcc/config/i386/t-linux64

# Create an empty directory inside the unpacked source code:
mkdir -v build
cd build

# Configure the build
CFLAGS='-fPIC' CXXFLAGS='-fPIC' \
    ../configure --prefix=/mere \
    --host=${SYS_REAL} \
    --build=${SYS_REAL} \
    --target=${SYS_FAKE} \
    --with-sysroot=/ \
    --with-newlib \
    --without-headers \
    --with-local-prefix=/mere \
    --with-native-system-header-dir=/mere/include \
    --disable-nls \
    --disable-shared \
    --disable-decimal-float \
    --disable-threads \
    --disable-libatomic \
    --disable-libgomp \
    --disable-libmpx \
    --disable-libquadmath \
    --disable-libssp \
    --disable-multilib \
    --disable-libvtv \
    --disable-libstdcxx \
    --enable-languages=c,c++

# Compile
make

# Install
make install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
