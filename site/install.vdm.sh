#!/bin/bash
set -xe

dest="/var/www/html/site"

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

#db="fizlesh.sqlite3"
#rm -f $db || true
#sqlite3 $db < dbinit.sql
#sqlite3 $db < unused-dbinit.sql
#sqlite3 $db < ../junk/fizlesh.ru-content/ank/anketas-2012.07.23.sql

sudo mkdir -p "$dest"
sudo rm -rf /var/www/html/site/*
sudo cp -a * "$dest/"
sudo cp -a ./fizlesh.ru-content "$dest/"
if ! [ -r "$dest/fizlesh.ru-content/ank/$db" ]; then
	echo "Database not exists, installing..."
	sudo cp $db "$dest/fizlesh.ru-content/ank/"
fi

sudo rm -rf "$dest/.prec/"*
sudo rm -rf "$dest/admin_doc/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo mkdir -p "$dest/admin_doc/.prec/"
sudo touch "$dest/"{.htaccess,settings.php,engine.log}
if [ "$1" = "-f" ] ; then
	sudo cp "$dest/install.nt.php" "$dest/install.php"
	sudo chown -R apache:apache "$dest/install.php"
fi
sudo chown -R apache:apache "$dest/"{.prec,fizlesh.ru-content,.htaccess,settings.php,engine.log}
sudo chown -R apache:apache "$dest/admin_doc/"{.prec,content,.htaccess,settings.php}
