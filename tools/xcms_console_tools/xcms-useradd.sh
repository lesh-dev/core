#!/usr/bin/env bash

print_usage()
{
    cat <<EOF
Usage: $0 <options> <user-email>"
    Options:
        -x, --xcms-home  XCMS Home
        -u, --user       User name
        -p, --password   User password
        -h, --help       This help
    Example:
        $0 -u ivanov -p i4OO-lcf7 ivanov.leonid@gmail.com
EOF
}

error_exit()
{
    msg="$1"
    if [ -n "Error: $msg" ] ; then
        echo "$msg"
    fi
    echo
    print_usage
}

if [ -z "$1" ]; then
    print_usage
    exit 1
fi
while [ true ]; do
    if [ -z "$1" ]; then
        break
    fi
    if [ "$1" == "-x" ] || [ "$1" == "--xcms-home" ]; then
        shift
        XCMS_HOME=$1
        shift
        continue
    fi
    if [ "$1" == "-p" ] || [ "$1" == "--password" ]; then
        shift
        password=$1
        shift
        continue
    fi
    if [ "$1" == "-u" ] || [ "$1" == "--user" ] ; then
        shift
        login=$1
        shift
        continue
    fi
    if [ "$1" == "-h" ] || [ "$1" == "--help" ] ; then
        print_usage
        exit 1
    fi
    break
done
mail=$1
if [ -z "$mail" ]; then
    error_exit "No mail specified. "
fi
if [ -z "$XCMS_HOME" ]; then
    error_exit "No \$XCMS_HOME specified. Either set XCMS_HOME environment or set it from command line. "
fi
if [ -z "$login" ]; then
    login=$(echo $mail | sed 's/@.*//g' )
    echo "Login is not set. Autogenerating from email: '$login'"
    if [ -z "$login" ] ; then
        error_exit "Login autogenerating from email failed. Please check email format. "
    fi
fi
if [ -z "$password" ]; then
    password=$(echo "$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM" | md5sum | cut -c2-9)
    echo "Password: $password"
fi

sudo su www-data -c "php $(dirname $0)/xcms.php  basedir=$XCMS_HOME useradd login=$login password=$password mail=$mail groups=editor,ank notify=yes"
