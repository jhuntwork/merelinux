#!/bin/sh -e
do_clean=0
lxcdir=/var/lib/lxc
template=merebuild
rootfs="${lxcdir}/${template}/rootfs"
home="${rootfs}/merebuild"
shome="/${home##*/}"
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

cleanup() {
    if [ $1 -eq 1 ] ; then
        info "Removing existing ${template} container"
        lxc-destroy -n ${template} >/dev/null 2>&1 || true
    fi
}

while getopts "cp:" arg ; do
    case $arg in
        c) do_clean=1 ;;
        p)
            pkgdir="$OPTARG"
            [ -d "$pkgdir" ] || error "Missing directory: ${pkgdir}"
            ;;
    esac
done

trap "cleanup ${do_clean}" INT EXIT

[ $do_clean -eq 1 ] && exit 0
[ -n $pkgdir ] || error "Package directory required"

cleanup 1

info "Creating a fresh ${template} container"
lxc-create -n ${template} -t ${template} >$clog 2>&1 ||
    error "Failed to create container. Examine ${clog} for details."

info "Copying package definition to container"
cd "$pkgdir"
find ! -type d -maxdepth 1 | cpio -dumpv "${home}/" >>$clog 2>&1

info "Building package"
lxc-start -n ${template} -F -- /bin/sh -c \
    "mount -t proc proc /proc &&
     mount -t sysfs sysfs /sys &&
     /bin/sudo -u nobody -- \
     /bin/env -i PATH=/bin:/sbin TERM=$TERM \
     http_proxy=${http_proxy} \
     https_proxy=${https_proxy} \
     HOME=${shome} /bin/sh -c \
     'cd ${shome} &&
      makepkg ${sign} -fLs --noconfirm'"
