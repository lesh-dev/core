#!/bin/bash
set -xe

dest="/var/www/html/site"

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

db="fizlesh.sqlite3"
rm -f $db || true
#sqlite3 $db < dbinit.sql
#sqlite3 $db < unused-dbinit.sql
#sqlite3 $db < ../junk/fizlesh.ru-content/ank/anketas-2012.07.23.sql
cp ../junk/fizlesh.ru-content/ank/lesh-2012.08.30.sqlite3 $db
#cp /var/www/html/site/fizlesh.ru-content/ank/fizlesh.sqlite3 complete.sql
#cp complete.sql $db

sudo mkdir -p "$dest"
sudo rm -rf /var/www/html/site/*
sudo cp -a * "$dest/"
sudo cp -a ../junk/fizlesh.ru-content "$dest/"
sudo cp $db "$dest/fizlesh.ru-content/ank/"
sudo rm -rf "$dest/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo touch "$dest/"{.htaccess,settings.php,engine.log}
if [ "$1" = "-f" ] ; then
    sudo touch "$dest/install.php"
    sudo chown -R apache:apache "$dest/install.php"
fi
sudo chown -R apache:apache "$dest/"{.prec,fizlesh.ru-content,.htaccess,settings.php,engine.log}
