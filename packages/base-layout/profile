# A generic personal profile settings file
# intended to be usable by mksh and bash

# Defaults
ps1_h=$(hostname -s)
ps1_c='\033[38;5;74m'
ps1_p='$'
PATH='/usr/local/bin:/bin:/usr/bin'

[ -z "$TERM" ] && TERM=linux
[ -z "$PAGER" ] && PAGER=less
[ -z "$EDITOR" ] && EDITOR=vi

# Special cases for root
if [ "$(id -u)" -eq 0 ] ; then
    ps1_p='#'
    ps1_c='\033[38;5;202m'
    PATH='/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin'
fi

set_ps1() {
    winsize=$(stty size)
    export COLUMNS=${winsize##* }
    printf '%d %s %s %b%s%b\n%s ' \
        "$?" "$ps1_h" "$(date +%T)" "$ps1_c" "$PWD" '\033[00m' "$ps1_p"
}

PS1='$(set_ps1)'
PS2=" > "


# export environment variables
export PATH TERM PAGER EDITOR
