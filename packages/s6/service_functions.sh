get_columns() {
    stty -a | grep -o columns\ [0-9]*\; | grep -o [0-9]*
}

display_ok() {
    N="\033[00m"
    C="\033[32m"
    len=$(printf "$@" | wc -m)
    col=$(get_columns)
    space=$(expr $col - $len - 7)
    printf "% ${space}s[ ${C}OK${N} ]\n"
}

display_fail() {
    N="\033[00m"
    C="\033[31m"
    len=$(printf "$@" | wc -m)
    col=$(get_columns)
    space=$(expr $col - $len - 9)
    printf "% ${space}s[ ${C}FAIL${N} ]\n"
}

usage() {
    printf "Usage: %s [service_name] [start|stop|status|restart]\n" $0
    exit 1
}

check_args() {
    [ $# -ne 2 ] && usage
    case "$2" in
        start|stop|status|restart) break ;;
        *) usage ;;
    esac
}

is_service() {
    if ! s6-svok "/service/${1}" ; then
        printf "%s is not a supervised service\n" $1
        exit 1
    fi
}
