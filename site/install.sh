#!/bin/bash
set -xe

dest="/var/www/html/site"

if [ -n "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

sudo cp -a * "$dest/"
sudo rm -rf "$dest/.prec/"*
sudo rm -rf "$dest/admin_doc/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo mkdir -p "$dest/admin_doc/.prec/"
sudo chmod 777 "$dest/.prec"
sudo touch "$dest/"{.htaccess,install.php,settings.php}
sudo chown -R apache:apache "$dest/"{fizlesh.ru-content,.htaccess,install.php,settings.php}
