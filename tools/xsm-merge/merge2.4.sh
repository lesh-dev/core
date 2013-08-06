#/usr/bin/env bash
set -e

new="fizlesh.sqlite3"
mode="$1"

if [ "$mode" == "installed" ] ; then
    cp /var/www/html/site/fizlesh.ru-content/ank/fizlesh.sqlite3 .
elif [ "$mode" == "local" ] ; then
    echo "Using current database"
else
    echo "Copying current production database"
    scp fizlesh.ru:/srv/www/production/content/ank/fizlesh.sqlite3 fizlesh.sqlite3
fi

echo "Run merger v2.3..."
php merger-v2.3-to-v2.4.php
