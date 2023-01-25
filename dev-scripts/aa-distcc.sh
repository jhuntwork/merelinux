#!/bin/bash
[ -n "$LIBMAKEPKG_TIDY_DISTCC_SH" ] && return
LIBMAKEPKG_TIDY_DISTCC_SH=1

LIBRARY=${LIBRARY:-'/usr/share/makepkg'}

# shellcheck disable=SC1091
source "$LIBRARY/util/message.sh"
# shellcheck disable=SC1091
source "$LIBRARY/util/option.sh"

packaging_options+=('distcc')
tidy_remove+=('tidy_distcc')

tidy_distcc() {
    if [ -n "$DISTCC_HOSTS" ] && [ ! -f /tmp/signalled-distcc ]; then
        for host in $DISTCC_HOSTS; do
            [ "$host" = 'localhost' ] && continue
            msg2 "$(gettext "Sending done signal to ${host%:*}...")"
            echo 'done' | nc "${host%:*}" 40001
        done
        touch /tmp/signalled-distcc
    fi
}
