N="\033[00m"
SVCS_DIR="/run/service"
AVAIL_DIR="/etc/s6/services/available"
ENABL_DIR="/etc/s6/services/enabled"

get_columns() {
    stty -a | grep -o columns\ [0-9]*\; | grep -oE '[0-9]*'
}

display_ok() {
    C="\033[32m"
    len=$(printf "$@" | wc -m)
    col=$(get_columns)
    space=$(expr $col - $len - 7)
    printf "% ${space}s[ ${C}OK${N} ]\n"
}

display_fail() {
    C="\033[31m"
    len=$(printf "$@" | wc -m)
    col=$(get_columns)
    space=$(expr $col - $len - 9)
    printf "% ${space}s[ ${C}FAIL${N} ]\n"
}

usage() {
    USAGE="
  Usage:
    %s list
    %s <service_name> [command]

  Commands:
    enable   Enables and attempts to start a service
    disable  Disables and attempts to stop a service
    start    Attempt to start a service
    stop     Attempt to stop a service
    status   Show status of a service
    reload   Signal the service to reload its configuration
    restart  Stop and then start a service

"
    printf "$USAGE" $0 $0
    exit 1
}

check_args() {
    if [ "$1" = "list" ] ; then
        list_services
    else
        [ $# -ne 2 ] && usage
        case "$2" in
            enable|disable|start|stop|status|reload|restart)
                svc=$1
                act=$2
                svcdir="${SVCS_DIR}/${svc}"
                export svc act svcdir
                break
                ;;
            *) usage ;;
        esac
    fi
}

is_supervised() {
    if ! s6-svok $svcdir ; then
        printf "%s is not a supervised service\n" ${svc}
        exit 1
    fi
}

is_service() {
    if [ ! -x ${AVAIL_DIR}/${svc}/run ] ; then
        printf "%s is not an available service\n" ${svc}
        exit 1
    fi
}

run_cmd() {
    printf "%s" "$message"
    if $1 ; then
        display_ok "$message"
    else
        display_fail "$message"
    fi
}

list_services() {
    LIST="Service Enabled Status ------- ------- ------- "
    for dir in $(find ${AVAIL_DIR} -type d -mindepth 1 -maxdepth 1 | sort | xargs) ; do
        bn=${dir##*/}
        LIST="$LIST ${bn} "
        if [ -e "${ENABL_DIR}/${bn}" ] ; then
            LIST="$LIST enabled "
            status=$(s6-svstat -n ${SVCS_DIR}/${bn} | cut -d' ' -f1)
            if echo $status | grep -q up ; then
                LIST="$LIST up "
            elif echo $status | grep -q down ; then
                LIST="$LIST down "
            else
                LIST="$LIST unknown "
            fi
        else
            LIST="$LIST disabled disabled "
        fi
    done
    printf "%-30s%-30s%s\n" $LIST
    exit 0
}
