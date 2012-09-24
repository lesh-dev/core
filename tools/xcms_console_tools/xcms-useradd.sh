#!/bin/bash
if [ $1. == . ]; then
    echo "$0 [-x xcms_home] [-u username] [-p password] user_email@example.com ";
    exit 1
fi
while [ true ]; do
  if [ $1. == . ]; then
    break;
  fi
  if [ $1. == "-x". ]; then
    shift
    XCMS_HOME=$1
    shift
    continue
  fi
  if [ $1. == "-p". ]; then
    shift
    password=$1
    shift
    continue
  fi
  if [ $1. == "-u". ]; then
    shift
    login=$1
    shift
    continue
  fi
  break 
done
mail=$1
if [ $mail. == . ]; then
  echo "No mail specified"
  exit 1
fi
if [ $XCMS_HOME. == . ]; then
  echo "No XCMS_HOME specified. Abort."
  exit 1
fi
if [ $login. == . ]; then
  login=$(echo $mail | sed s/"@.*"//g )
  echo "User's login: $login"
fi
if [ $password. == . ]; then
  password=$(echo "$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM" | md5sum | cut -c2-9)
  echo "Password: $password"
fi

sudo su www-data -c "php $(dirname $0)/xcms.php  basedir=$XCMS_HOME useradd login=$login password=$password mail=$mail groups=editor,ank notify=yes"

