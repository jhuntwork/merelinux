#!/bin/bash
# First convert any hardlinks to softlinks
files=$(find "$@/usr/share/man" -type f)
files=$(ls -i $files | sort)
IFS='
'
oldinode=""
for file in $files ; do
  inode=${file%* *}
  file=${file#* *}
  if [ "${inode}" = "${oldinode}" ] ; then
     common=$file
     back=''
     count=0
     while [ "${oldfile#$common}" = "${oldfile}" ] ; do
        common="${common%/*.*}"
        if [ $count -ge 1 ] ; then
           back="../${back}"
        fi
        let "count++"
     done
     link="${back}${oldfile#$common/}"
     rm -f "$file"
     ln -s "$link" "$file"
  else
     oldfile=$file
     oldinode=$inode
  fi
done

# Next compress any real files left
find "$@/usr/share/man" -type f -exec bzip2 -9 '{}' \;

# Finally rename any softlinks to their bz2 name
for i in $(find "$@/usr/share/man" -type l) ; do
    link=$(basename `readlink $i`)
    fn=$(basename $i)
    dn=$(dirname $i)
    rm -f $i
    ln -s $link.bz2 "$dn/$fn.bz2"
done
