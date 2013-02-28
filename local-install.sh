#!/bin/bash

VERBOSE_COPY=""

function do_prepare_installer
{
	INST_DEST="$1"
	if [ -z "$INST_DEST" ]; then
		echo "Parameter for do_prepare_installer not set. "
		return 1
	fi
        sudo cp $VERBOSE_COPY "$dest/install.nt.php" "$dest/install.php"
        sudo chown -R apache:apache "$dest/install.php"
}

set -e

if ! which sqlite3 > /dev/null; then
	echo "Please install SQLite v.3 on your machine. "
	exit 1
fi

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
	echo "This script installs XCMS to local www root. "
	exit 1
fi

dest="/var/www/html/site"

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

REPO_NAME="content-fizlesh.ru"

CONT_DIR="../$REPO_NAME/content"
DEST_CONT="fizlesh.ru-content"

if ! [ -d "$CONT_DIR" ]; then
        echo "Content directory not found, exiting. "
        echo "It should be 2 dir-levels above and called fizlesh.ru-content."
        exit 1
fi

echo "Preparing XSM database. "
xsm_db="fizlesh.sqlite3"

sudo mkdir -p "$dest"
# double-check that we are not doing something awful.

DB_SUBDIR="$DEST_CONT/ank"
TEMP_DB="/tmp/xcms_local_installer_$$_$xsm_db"
DEST_DB="$dest/$DB_SUBDIR/$xsm_db"

if [ -r "$DEST_DB" ]; then
        echo "Database already exists, backuping it."
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
sudo cp -a $VERBOSE_COPY site/* "$dest/"

sudo cp -a $VERBOSE_COPY $CONT_DIR "$dest/$DEST_CONT"

if [ -r "$TEMP_DB" ]; then
	echo "Backuped database exists, installing..."
	sudo mv $TEMP_DB "$DEST_DB"
else
	echo "No database found, creating fresh database. "
	TEMP_DB="/tmp/temp_$$_$xsm_db"
	rm -f $TEMP_DB || true
	sqlite3 $TEMP_DB < ./site/engine/dbpatches/dbinit-v2.sql
	sudo cp $VERBOSE_COPY $TEMP_DB $DEST_DB
fi

echo "Cleaning temporary stuff and caches. "

sudo rm -rf "$dest/.prec/"*
#sudo rm -rf "$dest/admin_doc/.prec/"*
sudo mkdir -p "$dest/.prec/"
#sudo mkdir -p "$dest/admin_doc/.prec/"
sudo touch "$dest/"{.htaccess,engine.log}

if ! [ -r $dest/site/settings.php ]; then
	echo "Seems that installation is performed for a first time. "
	echo "So You should go through XCMS install process. "
	do_prepare_installer $dest
fi

if [ "$1" = "-i" ] || [ "$1" = "--installer" ]; then
	echo "Forcing installer preparation. "
	do_prepare_installer "$dest"
fi

echo "Changing root password to 'root'..."
# change root password to 'root'
sudo cp -f $VERBOSE_COPY ./tools/xcms_console_tools/root_root_user $dest/$DEST_CONT/auth/usr/root.user

sudo chown -R apache:apache "$dest"   # why all this shit needed?! We need to set apache rules for ALL <www-root>/site ! ### CRAP {.prec,$DEST_CONT,.htaccess,settings.php,install.nt.php,engine.log} CRAP ###
# got error on this line. I don't have this directory in repo!

#sudo chown -R apache:apache "$dest/admin_doc/"{.prec,content,.htaccess,settings.php}

echo "XCMS installed to http://localhost/site"

