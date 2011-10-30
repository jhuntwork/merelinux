#!/bin/bash
URL=https://dev.lightcube.us/api/

usage_header() {
  echo -e "$0 :: A tool to update the LightCube OS RPM repositories\n"
}

main_usage() {
  usage_header
  echo "Usage: $0 {add|delete|help|promote|update}"
}

help_usage() {
  usage_header
  echo "Usage: $0 help [subcommand]"
  echo -e "\nPossible subcommands:\n"
  echo "add     :: Add a new package to the dev RPM repository"
  echo "delete  :: Remove a package from the dev RPM repository"
  echo "promote :: Promote the dev RPM repository to the testing RPM repository, or promote the testing RPM repository to the stable RPM repository"
  echo "update  :: Update an existing package in the dev RPM repository"
  echo 
}

update_usage() {
  usage_header
  echo "Reads info from an RPM spec file to update an existing package in the dev RPM repository."
  echo -e "Assumes that the spec file is up to date and has already been used to build packages located in /usr/src/rpm/{S,}RPMS\n"
  echo "Usage: $0 update [path/to/specfile]"
}

get_login() {
  echo -e "\nA request will be sent over HTTPS to dev.lightcube.us for processing"
  echo "Please enter your username and password."
  echo -e "Note: your password will not be shown on screen\n"
  echo -n "Username: "
  read user
  stty -echo
  echo -n "Password: "
  read pass
  stty echo
  echo
}

source_spec() {
  name=$(grep '^Name: ' $specfile | awk '{print $2}')
  version=$(grep '^Version: ' $specfile | awk '{print $2}')
  release=$(grep '^Release: ' $specfile | awk '{print $2}')
  arch=$(grep '^Buildarch: ' $specfile | awk '{print $2}')
  arch=${arch:-$(uname -m)}
  subpkgs=$(grep '^%package ' $specfile | awk '{print $2}')
  FILES="/usr/src/rpm/RPMS/${arch}/${name}-${version}-${release}.${arch}.rpm"
  FILES="${FILES} /usr/src/rpm/SRPMS/${name}-${version}-${release}.src.rpm"
  if [ ! -z "${subpkgs}" ] ; then
    for pkg in ${subpkgs} ; do
      subs="${subs} ${pkg}";
      FILES="${FILES} /usr/src/rpm/RPMS/${arch}/${name}-${pkg}-${version}-${release}.${arch}.rpm"
    done
  fi
  for file in ${FILES} ; do
    if [ ! -f ${file} ] ; then
      echo "No such file or directory: ${file}"
      missingfile=1
    fi
  done
  if [ "${missingfile}" = "1" ] ; then
    exit 1
  fi
}

# Verify a valid first param has been given
if [ -z "$1" ] ; then
  main_usage
  exit 1
fi

case $1 in
  add)
    echo "Not yet implemented"
    exit 0
  ;;

  delete)
    echo "Not yet implemented"
    exit 0
  ;;

  help)
    if [ -z "$2" ] ; then
      help_usage
      exit 1
    fi
    case $2 in
      add) echo "No help written for this section yet" ;;
      delete) echo "No help written for this section yet" ;;
      promote) echo "No help written for this section yet" ;;
      update) update_usage ;;
      *) help_usage ; exit 1 ;;
    esac
    exit 0
  ;;

  promote)
    echo "Not yet implemented"
    exit 0
  ;;

  update)
    if [ -z "$2" ] ; then
      update_usage
      exit 1
    fi
    if [ ! -f $2 ] ; then
      stat $2
    fi
    specfile=$2;
    get_login
    # Attempt a quick login before sending any files
    DATA="json={\"action\":\"check\",\"user\":\"$user\",\"pass\":\"$pass\"}"
    ret=$(curl --data-urlencode ${DATA} ${URL} 2>/dev/null)
    if [ "${ret}" = "OK" ] ; then
      source_spec
      for file in ${FILES} ; do
        files="${files} $(basename ${file})"
        echo "Uploading ${file}"
        curl --progress-bar -T ${file} ftp://dev.lightcube.us/jBM2irWIMpMQ/
        echo 
      done
      DATA="json={\"action\":\"update\",\"user\":\"$user\",\"pass\":\"$pass\",\"arch\":\"$arch\",\"files\":\"$files\",\"name\":\"$name\",\"subpkgs\":\"$subs\"}"
      echo -e "\nCreating the repository, sit tight for a few minutes...\n"
      curl --data-urlencode "${DATA}" ${URL}
    fi
  ;;  

  *) main_usage ; exit 1 ;;
esac
