#/usr/bin/env bash

new="new.v2.sqlite3"
rm $new

sqlite3 $new < engine/dbpatches/dbinit-v2.sql
# run merger
php merger.php
