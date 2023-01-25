#!/bin/bash -e
# shellcheck disable=SC2154,SC1091
bn="$(git rev-parse --abbrev-ref HEAD)"
if [ "$bn" != 'main' ] ; then
    . "$CIRCLE_WORKING_DIRECTORY"/.env
    if [ -n "$pkg" ] && [ "$is_deleted" = 'false' ]; then

        if printf '%s' "$bn" | grep -qE '^.*-parallel$'; then

            DISTCC_PORT='40000'
            DISTCC_CIDR='172.0.0.0/8'

            curl -fsSL https://tailscale.com/install.sh | sudo sh
            sudo tailscale up --authkey="$TS_KEY" \
                --hostname="mereci-${CIRCLE_BUILD_NUM}-${CIRCLE_NODE_TOTAL}-${CIRCLE_NODE_INDEX}"

            case "$CIRCLE_NODE_INDEX" in
                0)
                    DISTCC_HOSTS='localhost'
                    step=1
                    while [ "$step" -lt "$CIRCLE_NODE_TOTAL" ]; do
                        peerip=$(dig +short "mereci-${CIRCLE_BUILD_NUM}-${CIRCLE_NODE_TOTAL}-${step}.bonobo-bluegill.ts.net")
                        until [ -n "$peerip" ]; do
                            sleep 5
                            peerip=$(dig +short "mereci-${CIRCLE_BUILD_NUM}-${CIRCLE_NODE_TOTAL}-${step}.bonobo-bluegill.ts.net")
                        done
                        DISTCC_HOSTS="${DISTCC_HOSTS} ${peerip}:${DISTCC_PORT}"
                        step=$((step + 1))
                    done
                    cat >.build-env <<-EOF
					DISTCC_HOSTS=$DISTCC_HOSTS
					CC=/usr/lib/distcc/cc
					CXX=/usr/lib/distcc/c++
					EOF
                    MEREDIR="/tmp/mere" ./buildpkg.sh "$pkg"
                    ;;
                *)
                    printf 'Listening on port %s\n' "$DISTCC_PORT"
                    docker run -t --rm \
                        -p "$DISTCC_PORT":"$DISTCC_PORT" -e DISTCC_PORT="$DISTCC_PORT" \
                        -e DISTCC_CIDR="$DISTCC_CIDR" mere/distcc &
                    # Listen on this port for any input to "signal" build job is finished
                    printf 'Listening for done signal on port 40001\n'
                    nc -l -p 40001
                    ;;

            esac
        else
            MEREDIR="/tmp/mere" ./buildpkg.sh "$pkg"
        fi
    else
        printf 'No packages are required to build in this commit.\n'
    fi
fi
