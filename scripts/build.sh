#!/bin/sh -e
shome="/tmp/wd"
clog=/var/log/merebuild.log
auto=0

msg() {
    printf "%s\n" "$1"
}

info() {
    msg "INF: $1"
}

error() {
    msg "ERR: $1"
    exit 1
}

usage() {
    printf "
Usage: %s <pkgdir> [options]

  <pkgdir>   Identifies a directory containing, at minimum, a PKGBUILD file.
             The directory may also contain a ChangeLog file and additional
             source files required for the build.

  -a,--auto  Run a container in the foreground, but non-interactively.
             Signals are ignored.

" "$0"
}

if [ -z "$1" ] || [ ! -d "$1" ] ; then
    usage
    error "Missing or invalid directory. pkgdir argument: ${pkgdir}"
else
    pkgdir=$(realpath "$1")
    name="merebuild-${pkgdir##*/}"
    shift
fi

if options=$(getopt -o a -l auto -- "$@" 2>&1); then
    eval set -- "$options"
    while true
    do
        case "$1" in
            -a|--auto) auto=1; shift 2;;
            --)        shift 1; break;;
            *)         break;;
        esac
    done
else
    usage
    error "$(printf "%s" "$options" | head -n1 | sed 's@getopt: @@')"
fi

# Make sure required mountpoints are present
mountpoint -q /sys/fs/cgroup || mount -t tmpfs cgroupfs /sys/fs/cgroup
awk '!/^#/ { if ($4 == 1) print $1 }' /proc/cgroups | \
    while IFS= read -r sys
do
    sys_path="/sys/fs/cgroup/${sys}"
    mkdir -p "$sys_path"
    mountpoint -q "$sys_path" ||
        mount -n -t cgroup -o "$sys" cgroup "$sys_path" ||
        rmdir "$sys_path" ||
        true
done

# Start fresh
info "Stopping and destroying any existing container named $name"
lxc-stop -k -n "$name" >/dev/null 2>&1 || true
lxc-destroy -n "$name" >/dev/null 2>&1 || true

# Create the container
info "Creating a fresh merebuild container named $name"
mere_package="$pkgdir" lxc-create -n "$name" -t merebuild >>"$clog" 2>&1 ||
    error "Failed to create container. Examine ${clog} for details."

# Execute the container
if [ $auto -eq 1 ] ; then
    [ -n "$mere_no_deps" ] && mere_no_deps='-d'
    info "Running the container"
    lxc-start -n "$name" -F -- \
        /bin/env -i TERM="$TERM" HOME="$shome" \
        /bin/sh -lc "cd ${shome} && makepkg -Ls --noconfirm ${mere_no_deps}"
else
    info "Entering the container"
    lxc-start -n "$name" -F -- \
    /bin/env -i TERM="$TERM" HOME="$shome" \
    /bin/sh -c "cd ${shome} && printf \"#!/bin/sh\nmakepkg -Ls\" >/bin/mp &&
        chmod +x /bin/mp &&
        printf \"\nReady.\nTo make the package, run %s\n\n\" \
        \"'makepkg -Ls', or its short equivalent, 'mp'\" && exec /bin/bash -l"

fi
