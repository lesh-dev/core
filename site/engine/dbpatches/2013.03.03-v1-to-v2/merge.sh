#/usr/bin/env bash
set -xe

new="new.v2.sqlite3"
rm -f $new

sqlite3 $new < ../dbinit-v2.sql
# run merger
cd ../../../
php merger-v1-to-v2.php
