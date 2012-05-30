#!/bin/bash
set -xe

dest="/var/www/html/site"

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

sudo rm -rf /var/www/html/site/*
sudo cp -a * "$dest/"
sudo rm -rf "$dest/.prec/"*
sudo rm -rf "$dest/admin_doc/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo mkdir -p "$dest/admin_doc/.prec/"
sudo touch "$dest/"{.htaccess,settings.php}
if [ "$1" = "-f" ] ; then
    sudo touch "$dest/install.php"
    sudo chown -R apache:apache "$dest/install.php"
fi
sudo chown -R apache:apache "$dest/"{.prec,fizlesh.ru-content,.htaccess,settings.php}
sudo chown -R apache:apache "$dest/admin_doc/"{.prec,content,.htaccess,settings.php}
