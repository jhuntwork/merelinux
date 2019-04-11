{% extends "buildpackage.sh" %}
{% block build %}
# Unpack the other libraries which will be included in this build:
{% for item in extra_filenames %}source_dir_{{item.name}}=$(unpack /mere/sources/{{item.filename}})
mv "${source_dir_{{item.name}}:?}" {{item.name}}

{% endfor %}# Adjust some of the included configuration files to point at the isolated
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

{% endblock %}
