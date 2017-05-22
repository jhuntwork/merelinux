#!/bin/sh -e
do_clean=0
shome="/tmp/wd"
clog=/tmp/merebuild.log

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

cleanup() {
    if [ $1 -eq 1 ] ; then
        info "Removing any existing container named $name"
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

[ -z "$mere_pacman_conf" ] && export mere_pacman_conf='/etc/pacman.conf'

info "Creating a fresh $name container"
mere_package="$pkgdir" lxc-create -n ${name} -t merebuild >$clog 2>&1 ||
    error "Failed to create container. Examine ${clog} for details."

info "Building package"
lxc-start -n ${name} -F -- /bin/env -i TERM=$TERM \
     http_proxy=${http_proxy} \
     https_proxy=${https_proxy} \
     SHELL=/bin/bash \
     HOME=${shome} /bin/sh -lc \
     "cd ${shome} &&
      makepkg -fLs --noconfirm"
