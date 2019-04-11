{% extends "buildpackage.sh" %}
{% block build %}
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
    --with-gxx-include-dir=/mere/${SYS_FAKE}/include/c++/{{version}}

# Compile
make

# Install
make install

# Perform another sanity check to ensure libstdc++ is working
echo 'int main(){return 0;}' | ${SYS_FAKE}-g++ -x c++ - -v -lrt -Wl,--verbose | tee output
grep '/mere.*c++.*succeeded' output
readelf -l a.out | grep /mere

{% endblock %}
