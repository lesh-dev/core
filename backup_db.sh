#!/usr/bin/env bash

if [ "$1" = "backup" ] ; then
    cp /var/www/vhosts/fizlesh.ru/fizlesh.ru-content/ank/fizlesh.sqlite3 .
elif [ "$1" = "install" ] ; then
    sudo cp fizlesh.sqlite3 /var/www/vhosts/fizlesh.ru/fizlesh.ru-content/ank/fizlesh.sqlite3
else
    echo "Usage: $0 <backup|install>"
    echo "In 'backup' mode it copies fizlesh.sqlite database into your current directory"
    echo "and in 'install' mode it restores it back"
fi
