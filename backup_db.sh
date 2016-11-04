#!/usr/bin/env bash

db="fizlesh.sqlite3"

set -e

if [ "$1" = "backup" ] ; then
    cp /var/www/vhosts/fizlesh.ru/fizlesh.ru-content/ank/$db .
    echo "Backed up successfully to ./$db"
elif [ "$1" = "install" ] ; then
    dest=/var/www/vhosts/fizlesh.ru/fizlesh.ru-content/ank/$db
    sudo cp $db $dest
    echo "Copied successfully from $db to $dest"
else
    echo "Usage: $0 <backup|install>"
    echo "In 'backup' mode it copies fizlesh.sqlite database into your current directory"
    echo "and in 'install' mode it restores it back"
fi

