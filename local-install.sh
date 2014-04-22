#!/usr/bin/env bash

set -e

# set this to -v to add some verbosity (or use -v switch)
VERBOSE=""

# database update mode
DB_MODE=original

# wwwroot owner/group (www or www-data on debian)
HTTPD_USER="apache"

# database file name
XSM_DB="fizlesh.sqlite3"

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

# configure rests of unset options
if [ -z "$DEST_NAME" ] ; then
    # default site location
    DEST_NAME="site"
    if [ "$USERNAME" == "mvel" ] ; then
        DEST_NAME="fizlesh.ru"
    fi
fi

# folder with content repo
REPO_NAME="content-fizlesh.ru"
if [ "$USERNAME" == "mvel" ] ; then
    REPO_NAME="content-$DEST_NAME"
fi

# content path
CONT_DIR="../$REPO_NAME/content"

# installed content folder name
DEST_CONT="fizlesh.ru-content"
if [ "$USERNAME" == "mvel" ] ; then
    DEST_CONT="$DEST_NAME-content"
fi


function do_prepare_installer()
{
    message "Forcing installer preparation"
    INST_DEST="$1"
    if [ -z "$INST_DEST" ]; then
        echo "Parameter for do_prepare_installer not set. "
        return 1
    fi
    sudo cp $VERBOSE "$DEST/install.nt.php" "$DEST/install.php"
    sudo chown -R $HTTPD_USER:$HTTPD_USER "$DEST/install.php"
}

function install_fresh_db()
{
    message "Creating fresh database"
    TEMP_DB="/tmp/temp_$$_$XSM_DB"
    rm -f $TEMP_DB || true
    sqlite3 $TEMP_DB < ./site/engine/dbpatches/dbinit-v2.sql
    sudo cp $VERBOSE $TEMP_DB $DEST_DB
}

# Copy-pasted from testing.receipe with -w -> -r modification
function xsm_clear_notifications()
{
    db="$DEST/$DEST_CONT/ank/fizlesh.sqlite3"
    if [ -r "$db" ] ; then
        echo 'DELETE FROM notification;' | sudo sqlite3 "$db"
        message "Notifications table cleared successfully"
    fi

    mc="$DEST/$DEST_CONT/cms/mailer.conf"
    if [ -r "$mc" ] ; then
        mail_test="vdm-photo@ya.ru"
        cat > "$mc" <<EOF
user-change:$mail_test
content-change:$mail_test
reg:$mail_test
reg-managers:$mail_test
reg-test:$mail_test
reg-managers-test:$mail_test
EOF
        message "Mailer config was reset to '$mail_test' address for each notification handler"
    fi

}

# site root
DEST="/var/www/html/$DEST_NAME"
if [ "$USERNAME" == "mvel" ] ; then
    DEST="/var/www/vhosts/$DEST_NAME"
fi

# check SQLite3 presence
if ! which sqlite3 > /dev/null; then
    message_error "Please install SQLite v.3 on your machine"
    exit 1
fi

if [ -z "$DEST" ] ; then
    message_error "Destination path cannot be empty"
    exit 1
fi

if ! [ -d "$CONT_DIR" ]; then
    message_error "Content directory not found, exiting. "
    message_error "It should be 2 dir-levels above and named '$DEST_CONT'."
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
DEST_CHECK="` echo -n $DEST | sed -e 's:/::g' `"
if ! [ -z "$DEST_CHECK" ]; then
    message "Cleaning destination directory $DEST"
    sudo rm -rf "$DEST/{doc,$DEST_CONT,fizlesh.ru-design,engine,engine_public}"
else
    message_error "Bug in your script!"
    exit 1
fi

message "Copying all stuff to destination. "
sudo cp -a $VERBOSE ./site/* "$DEST/"

# need to remove destination, otherwise it will be nested
sudo rm -rf "$DEST/$DEST_CONT"
sudo cp -a $VERBOSE $CONT_DIR "$DEST/$DEST_CONT"

VERSION="`tools/publish/version.sh`-local"
message "Set version: $VERSION"
VFILE=`mktemp`
echo "version : $VERSION" > $VFILE
sudo cp $VERBOSE $VFILE $DEST/INFO
rm -f $VFILE

message "Creating database target folder"
sudo mkdir -p $VERBOSE "$(dirname $DEST_DB)"

# process database
if [ "$DB_MODE" == "merged" ] ; then
    message "Installing merged database"
    sudo cp $VERBOSE tools/xsm-merge/new*sqlite3 $DEST_DB
elif [ "$DB_MODE" == "empty" ] ; then
    install_fresh_db
elif [ "$DB_MODE" == "original" ] ; then
    # if saved database exists, restore it,
    # otherwise database stored in original content
    # will be used
    if [ -r "$TEMP_DB" ] ; then
        message "Database backup found, installing..."
        sudo mv $TEMP_DB "$DEST_DB"
    fi
else
    print_usage
fi

message "Cleaning temporary stuff and caches"

sudo rm -rf "$DEST/.prec/"*
sudo mkdir -p "$DEST/.prec/"
sudo touch "$DEST/"{.htaccess,engine.log}

if ! [ -r $DEST/settings.php ]; then
    message "Seems that installation is performed for a first time. "
    message "So you should go through XCMS install process. "
    do_prepare_installer $DEST
fi

if [ "$PREPARE_INSTALLER" = "yes" ] ; then
    do_prepare_installer "$DEST"
fi

xsm_clear_notifications

message "Changing root password to 'root'..."
# change root password to 'root'
sudo cp -f $VERBOSE ./tools/xcms_console_tools/root_root_user $DEST/$DEST_CONT/auth/usr/root.user

sudo chown -R $HTTPD_USER:$HTTPD_USER "$DEST"

message_ok "XCMS installed to http://localhost/$DEST_NAME"
