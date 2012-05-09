#!/bin/bash
set -xe

dest="/var/www/html/site"

if [ -z "$dest" ] ; then
    echo "Destination path cannot be empty"
    exit 1
fi

sudo cp -a * "$dest/"
sudo rm -rf "$dest/.prec/"*
sudo rm -rf "$dest/admin_doc/.prec/"*
sudo mkdir -p "$dest/.prec/"
sudo mkdir -p "$dest/admin_doc/.prec/"
sudo touch "$dest/"{.htaccess,install.php,settings.php}
sudo chown -R apache:apache "$dest/"{.prec,fizlesh.ru-content,.htaccess,install.php,settings.php}
sudo chown -R apache:apache "$dest/admin_doc/"{.prec,.htaccess,settings.php}
