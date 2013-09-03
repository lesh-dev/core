#!/usr/bin/env bash

set -xe

# Migration script to 2.4 site version
# Place this script into $SITE_ROOT/migrate2.4/ folder

wd="$( pwd )"
site_root="$( dirname $wd )"
cd $site_root
content_dir="$( ls -d *content )"
cd "$wd"

echo "Site root is $site_root"

target_db="$site_root/$content_dir/ank/fizlesh.sqlite3"
sudo cp $target_db .

echo "Run merger v2.3..."
sudo cp settings2.4.php settings.php
sudo sed -i -e "s/@@CONTENT@/$content_dir/" settings.php
sudo php merger-v2.3-to-v2.4.php
sudo cp fizlesh.sqlite3 $target_db
