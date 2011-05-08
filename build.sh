#!/bin/bash
if [ -z $1 ] ; then
   echo "Usage: $0 [package name]"
   exit 1
fi
rpm -ba packages/$1/$1.spec 2>&1 | tee packages/$1/build.log
