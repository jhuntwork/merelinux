#!/bin/sh -e
do_clean=0
lxcdir=/var/lib/lxc
shome="/tmp/wd"
clog=/tmp/merebuild.log
sign=''

msg() {
    printf "%s\n" "$1"
}

info() {
    msg "INFO: $1"
}

error() {
    msg "ERROR: $1"
    exit 1
}

pkgdir="$1"
[ -d "$pkgdir" ] || error "Missing directory: ${pkgdir}"
pkgdir=$(realpath "$pkgdir")
name="merebuild-${pkgdir##*/}"
rootfs="${lxcdir}/${name}/rootfs"
wd="${rootfs}${shome}"

cleanup() {
    if [ $1 -eq 1 ] ; then
        info "Removing existing $name container"
        lxc-destroy -n $name >/dev/null 2>&1 || true
    fi
}

trap 'cleanup 0' INT EXIT

cleanup 1

if ! mountpoint /sys/fs/cgroup >/dev/null 2>&1 ; then
    mount -t tmpfs cgroupfs /sys/fs/cgroup
    for sys in $(awk '!/^#/ { if ($4 == 1) print $1 }' /proc/cgroups); do
        sys_path="/sys/fs/cgroup/${sys}"
        mkdir -p $sys_path
        if ! mountpoint -q $sys_path; then
            if ! mount -n -t cgroup -o $sys cgroup $sys_path; then
                rmdir $sys_path || true
            fi
        fi
    done
fi

info "Creating a fresh $name container"
mere_pacman_conf=/etc/pacman.conf \
    mere_package="$pkgdir" lxc-create -n ${name} -t merebuild >$clog 2>&1 ||
    error "Failed to create container. Examine ${clog} for details."

if [ -n "$MERE_PACKAGER" ] ; then
    info "Adding packager information to makepkg.conf"
    echo "PACKAGER='${MERE_PACKAGER}'" >>"${rootfs}/etc/makepkg.conf"
fi

ln -sf "${wd}" .
ln -sf "${rootfs}" .

info "Building package"
lxc-start -n ${name} -F -- /bin/env -i TERM=$TERM \
     http_proxy=${http_proxy} \
     https_proxy=${https_proxy} \
     SHELL=/bin/bash \
     HOME=${shome} /bin/sh -lc \
     "cd ${shome} &&
      makepkg ${sign} -fLs --noconfirm; sleep 1"
