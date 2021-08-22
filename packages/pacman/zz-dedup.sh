#!/bin/bash
#
#   dedup.sh - Find duplicate files and make them hard links
#
#   Copyright (c) 2021 Jeremy Huntwork <jhuntwork@lightcubesolutions.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

[ -n "$LIBMAKEPKG_TIDY_DEDUP_SH" ] && return
LIBMAKEPKG_TIDY_DEDUP_SH=1

LIBRARY=${LIBRARY:-'/share/makepkg'}

# shellcheck disable=SC1090
source "$LIBRARY/util/message.sh"
# shellcheck disable=SC1090
source "$LIBRARY/util/option.sh"

packaging_options+=('dedup')
tidy_modify+=('tidy_dedup')

tidy_dedup() {
	msg2 "$(gettext "De-duplicating files...")"
    if command -v fedup >/dev/null; then
        # shellcheck disable=SC2154
        fedup -q "$pkgdir"
        return $?
    fi
    IFS='
'
    # shellcheck disable=SC2154
    sumlist=$(find "$pkgdir" -type f -exec sha256sum '{}' +)

    # Get list of unique sums
    unique=$( (for item in $sumlist; do printf '%s\n' "${item% **}"; done) | sort -u)

    # De-dup - would be nicer if this was a hash table
    for sum in $unique ; do
        found=''
        for item in $sumlist ; do
            itemsum=${item% **}
            itemfile=${item##* }
            if [ "$sum" = "$itemsum" ]; then
                if [ -z "$found" ] ; then
                    found=$itemfile
                else
                    ln -f "$found" "$itemfile"
                fi
            fi
        done
    done
}
