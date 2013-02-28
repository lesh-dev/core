#/usr/bin/env bash
set -e

new="new.v2.sqlite3"

if ! [ "$1" = "--local" ] ; then
    echo "Copying current production database"
    scp fizlesh.ru:/srv/www/production/content/ank/fizlesh.sqlite3 current.v1.sqlite3
fi
echo "Initializing new database '$new'"
rm -f $new
sqlite3 $new < ../dbinit-v2.sql

echo "Run merger..."
cd ../../../
php merger-v1-to-v2.php
