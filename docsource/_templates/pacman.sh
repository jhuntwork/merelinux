{% extends "buildpackage.sh" %}
{% block build %}
# Remove some hard-coded references to /usr/bin in configure.ac as well
# as an unsupported flag for the busybox version of du
sed -i -e 's@/usr/bin/@@g' \
       -e 's@/usr/bin\$PATH_SEPARATOR@@g' \
       -e 's@ --apparent-size@@' configure.ac

# Some tweaks to the makepkg scripts
sed -i -e '/x-cpio/s@)@|*application/x-empty*)@' \
    scripts/libmakepkg/source/file.sh.in
sed -i -e 's/EUID == 0/EUID == -1/' \
    -e 's/-S --asdeps/--force &/' \
    scripts/makepkg.sh.in

# Generate the configure script
./autogen.sh

# Configure the build
./configure --prefix=/mere \
    --disable-doc \
    --disable-nls

# Compile
make

# Install
make install

# Create a usable pacman.conf configuration file
mv /mere/etc/pacman.conf{,.bak}
cat >/mere/etc/pacman.conf <<EOF
[options]
Architecture = auto
DBPath       = /var/lib/pacman
HoldPkg      = pacman busybox
CheckSpace

[buildlocal]
Server = file:///mere/pkgs
EOF

# Install a fake fakeroot script
install -m0755 /mere/sources/merelinux/packages/pacman/fakeroot \
    /mere/bin/fakeroot

# Override the default makepkg configuration
install -m0755 /mere/sources/merelinux/packages/pacman/makepkg.conf \
    /mere/etc/makepkg.conf

{% endblock %}
