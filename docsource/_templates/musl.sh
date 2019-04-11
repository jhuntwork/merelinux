{% extends "buildpackage.sh" %}
{% block build %}
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

{% endblock %}
