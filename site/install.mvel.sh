#!/usr/bin/env bash
set -xe

dest_name="site"
if [ "$HOSTNAME" == "blackbox" ] ; then
    dest_name="lesh"
fi
dest="/var/www/html/$dest_name"

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

content_name="fizlesh.ru-content"
db="fizlesh.sqlite3"
rm -f $db || true
sqlite3 $db < engine/dbpatches/dbinit-v2.sql
#sqlite3 $db < unused-dbinit.sql
#sqlite3 $db < ../junk/$content_name/ank/anketas-2012.07.23.sql
#cp ../junk/$content_name/ank/lesh-2012.08.30.sqlite3 $db
#cp /var/www/html/$dest_name/$content_name/ank/fizlesh.sqlite3 complete.sql
#cp complete.sql $db

sudo mkdir -p "$dest"
sudo rm -rf /var/www/html/$dest_name/*
sudo cp -a * "$dest/"
sudo mkdir -p "$dest/$content_name"
sudo cp -a ../../content-fizlesh.ru/content/* "$dest/$content_name/"
sudo cp $db "$dest/$content_name/ank/"
# hack mailer conf
sudo cp ../junk/$content_name/cms/mailer.conf "$dest/$content_name/cms/mailer.conf"
sudo rm -rf "$dest/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo touch "$dest/"{.htaccess,settings.php,engine.log}
if [ "$1" = "-f" ] ; then
    sudo mv "$dest/install.nt.php" "$dest/install.php"
    sudo chown -R apache:apache "$dest/install.php"
fi
sudo chown -R apache:apache "$dest/"{.prec,"$content_name",.htaccess,settings.php,engine.log}
