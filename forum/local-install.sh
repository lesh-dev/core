#!/usr/bin/env bash

set -e

# set this to -v to add some verbosity (or use -v switch)
VERBOSE=""

# wwwroot owner/group (www or www-data on debian)
HTTPD_USER="apache"

function message()
{
    echo -e "[\033[33mINSTALL\x1b[0m] $@"
}

function message_ok()
{
    echo -e "[\033[32mINSTALL\x1b[0m] $@"
}

function message_error()
{
    echo -e "[\033[31mINSTALL\x1b[0m] $@"
}


function print_usage()
{
    echo "Install XCMS to local www root."
    echo "Usage: `basename $0` <options>"
    echo "          [-i|--installer]       Force installer installation"
    echo "          [-v|--verbose]         Verbose mode"
    echo "          [-d|--db-mode] <mode>  DB install mode:"
    echo "                   original      Save original database (default)"
    echo "                   empty         Init fresh database using dbinit"
    echo "                   merged        Install merged database"
    echo "          [-p|--path] <name>     Change destination to <name>"
    echo "          [-h|--help]            This help"
    exit 1
}

# read options
while [ -n "$1" ]; do
    ARG="$1"
    if [ "$ARG" = "-h" ] || [ "$ARG" = "--help" ]; then
        print_usage
    elif [ "$ARG" = "-v" ] || [ "$ARG" = "--verbose" ]; then
        VERBOSE="-v"
    elif [ "$ARG" = "-d" ] || [ "$ARG" = "--db-mode" ]; then
        shift || true
        DB_MODE="$1"
    elif [ "$ARG" = "-i" ] || [ "$ARG" = "--installer" ]; then
        PREPARE_INSTALLER="yes"
    elif [ "$ARG" = "-p" ] || [ "$ARG" = "--path" ]; then
        shift || true
        DEST_NAME="$1"
    fi
    shift || true
done

user="$SUDO_USER"
if [ -z "$user" ] ; then
    user="$USER"
fi
message "User detected: $user"

# configure rests of unset options
if [ -z "$DEST_NAME" ] ; then
    # default site location
    DEST_NAME="forum.fizlesh.ru"
fi

# site root
DEST="/var/www/html/$DEST_NAME"
if [ "$user" == "mvel" ] ; then
    DEST="/var/www/vhosts/$DEST_NAME"
fi

# check MySQL presence
if ! which mysql > /dev/null; then
    message_error "Please install MySQL client on your machine"
    exit 1
fi

if [ -z "$DEST" ] ; then
    message_error "Destination path cannot be empty"
    exit 1
fi

message "Preparing XSM database. "

sudo mkdir -p  $VERBOSE "$DEST"

DB_SUBDIR="$DEST_CONT/ank"
TEMP_DB="/tmp/xcms_local_installer_$$_$XSM_DB"
DEST_DB="$DEST/$DB_SUBDIR/$XSM_DB"

if [ -r "$DEST_DB" ]; then
    message "Database already exists, backing it up."
    sudo cp $VERBOSE "$DEST_DB" "$TEMP_DB"
fi

# double-check that we are not doing something awful:
# ensure that DEST with removed slashes is not empty
# to avoid 'sudo rm -rf /'
DEST_CHECK="` echo -n $DEST | sed -e 's:[/.]::g' `"
if [ -n "$DEST_CHECK" ]; then
    message "Cleaning destination directory $DEST"
    sudo rm -rf "$DEST/*"
else
    message_error "Bug in your script!"
    exit 1
fi

message "Copying all stuff to destination. "
sudo cp -a $VERBOSE ./* "$DEST/"

sudo chown -R $HTTPD_USER:$HTTPD_USER "$DEST"

message_ok "FizLesh Forum installed to http://localhost/$DEST_NAME"
