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

# Install a more complete internal limits.h header into the cross-compiler's
# internal search path
cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
    $(dirname $(${SYS_FAKE}-gcc -print-libgcc-file-name))/include-fixed/limits.h

# Don't let gcc attempt to 'fix' any system headers
sed -i 's,\./fixinc\.sh,-c true,' gcc/Makefile.in

# Create an empty directory inside the unpacked source code:
mkdir -v build
cd build

# Configure the build
CFLAGS='-fPIC' \
    CXXFLAGS='-fPIC' \
    CC=${SYS_FAKE}-gcc \
    CXX=${SYS_FAKE}-g++ \
    AR=${SYS_FAKE}-ar \
    RANLIB=${SYS_FAKE}-ranlib \
    ../configure --prefix=/mere \
    --build=${SYS_REAL} \
    --host=${SYS_REAL} \
    --target=${SYS_REAL} \
    --with-local-prefix=/mere \
    --with-native-system-header-dir=/mere/include \
    --disable-shared \
    --disable-multilib \
    --disable-libgomp \
    --disable-bootstrap \
    --disable-libsanitizer \
    --disable-libstdcxx-pch \
    --enable-languages=c,c++

# Compile
make

# Install
make install
ln -sv gcc /mere/bin/cc

# Sanity check
echo 'int main(){return 0;}' | /mere/bin/cc -x c - -static -v -lrt -Wl,--verbose -Wl,-static
./a.out
echo 'int main(){return 0;}' | /mere/bin/cc -x c - -v -lrt -Wl,--verbose
readelf -l a.out | grep /mere

{% endblock %}
