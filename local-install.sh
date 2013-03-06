#!/usr/bin/env bash

set -e

# set this to -v to add some verbosity
VERBOSE_COPY=""

dest_name="site"
if [ "$HOSTNAME" == "blackbox" ] ; then
    dest_name="lesh"
fi

# site root
dest="/var/www/html/$dest_name"
# name of the folder with content repo
REPO_NAME="content-fizlesh.ru"
# content path
CONT_DIR="../$REPO_NAME/content"
# installed content folder name
DEST_CONT="fizlesh.ru-content"
# wwwroot owner/group (www or www-data on debian)
httpd_user="apache"
# database file name
xsm_db="fizlesh.sqlite3"

function print_usage()
{
    echo "Install XCMS to local www root."
    echo "Usage: $(basename $0) <options>"
    echo "          [-i|--installer]       Force installer installation"
    echo "          [-v|--verbose]         Verbose mode"
    echo "          [-d|--db-mode] <mode>  DB install mode:"
    echo "                   original      Save original database (default)"
    echo "                   empty         Init fresh database using dbinit"
    echo "                   merged        Install merged database"
    echo "          [-h|--help]            This help"
    exit 1
}

function do_prepare_installer()
{
    echo "Forcing installer preparation. "
    INST_DEST="$1"
    if [ -z "$INST_DEST" ]; then
        echo "Parameter for do_prepare_installer not set. "
        return 1
    fi
    sudo cp $VERBOSE_COPY "$dest/install.nt.php" "$dest/install.php"
    sudo chown -R $httpd_user:$httpd_user "$dest/install.php"
}

function install_fresh_db()
{
    echo "Creating fresh database. "
    TEMP_DB="/tmp/temp_$$_$xsm_db"
    rm -f $TEMP_DB || true
    sqlite3 $TEMP_DB < ./site/engine/dbpatches/dbinit-v2.sql
    sudo cp $VERBOSE_COPY $TEMP_DB $DEST_DB
}

# read options
while [ -n "$1" ]; do
    arg="$1"
    if [ "$arg" = "-h" ] || [ "$arg" = "--help" ]; then
        print_usage
    elif [ "$arg" = "-v" ] || [ "$arg" = "--verbose" ]; then
        VERBOSE_COPY="-v"
    elif [ "$arg" = "-d" ] || [ "$arg" = "--db-mode" ]; then
        shift || true
        db_mode="$1"
    elif [ "$arg" = "-i" ] || [ "$arg" = "--installer" ]; then
        prepare_installer="yes"
    fi
    shift || true
done

# check SQLite3 presence
if ! which sqlite3 > /dev/null; then
    echo "Please install SQLite v.3 on your machine. "
    exit 1
fi

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

if ! [ -d "$CONT_DIR" ]; then
    echo "Content directory not found, exiting. "
    echo "It should be 2 dir-levels above and named '$DEST_CONT'."
    exit 1
fi

echo "Preparing XSM database. "

sudo mkdir -p "$dest"
# double-check that we are not doing something awful.

DB_SUBDIR="$DEST_CONT/ank"
TEMP_DB="/tmp/xcms_local_installer_$$_$xsm_db"
DEST_DB="$dest/$DB_SUBDIR/$xsm_db"

if [ -r "$DEST_DB" ]; then
    echo "Database already exists, backing it up."
    sudo cp $VERBOSE_COPY "$DEST_DB" $TEMP_DB
fi

if ! [ -z "$dest" ]; then
    echo "Cleaning dest directory $dest"
    sudo rm -rf "$dest/{doc,$DEST_CONT,fizlesh.ru-design,engine,engine_public}"
else
    echo "Bug in your script!"
    exit 1
fi

echo "Copying all stuff to destination. "
sudo cp -a $VERBOSE_COPY ./site/* "$dest/"

sudo cp -a $VERBOSE_COPY $CONT_DIR "$dest/$DEST_CONT"

version="$(tools/publish/version.sh)-local"
echo "Set version: $version"
echo "version : $version" > /tmp/INFO
sudo cp $VERBOSE_COPY /tmp/INFO $dest/INFO

# process database
if [ "$db_mode" == "merged" ] ; then
    echo "Installing merged database"
    sudo cp $VERBOSE_COPY tools/xsm-merge/new*sqlite3 $DEST_DB
elif [ "$db_mode" == "empty" ] ; then
    install_fresh_db
elif [ "$db_mode" == "original" ] || [ -r "$TEMP_DB" ] ; then
    echo "Database backup found, installing..."
    sudo mv $TEMP_DB "$DEST_DB"
else
    print_usage
fi

echo "Cleaning temporary stuff and caches. "

sudo rm -rf "$dest/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo touch "$dest/"{.htaccess,engine.log}

if ! [ -r $dest/settings.php ]; then
    echo "Seems that installation is performed for a first time. "
    echo "So you should go through XCMS install process. "
    do_prepare_installer $dest
fi

if [ "$prepare_installer" = "yes" ] ; then
    do_prepare_installer "$dest"
fi

echo "Changing root password to 'root'..."
# change root password to 'root'
sudo cp -f $VERBOSE_COPY ./tools/xcms_console_tools/root_root_user $dest/$DEST_CONT/auth/usr/root.user

sudo chown -R $httpd_user:$httpd_user "$dest"
# why all this shit needed?! We need to set apache rules for ALL <www-root>/site !
### CRAP {.prec,$DEST_CONT,.htaccess,settings.php,install.nt.php,engine.log} CRAP ###
# got error on this line. I don't have this directory in repo!

echo "XCMS installed to http://localhost/site"
