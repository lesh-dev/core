#!/usr/bin/env bash

set -xe

uid="$(id -u)"
if [ "$1" != "--sudo" ] && [ "$uid" != "0" ] ; then
    echo "Migration should be run under root user"
    exit 1
fi

# Migration script to 2.8 site version
# Place this script into $SITE_ROOT/migrate2.8/ folder

wd="$( pwd )"
site_root="$( dirname $wd )"
cd $site_root
content_dir="$( ls -d *content )"
cd "$wd"

httpd_user="www-data"
if grep -q apache /etc/passwd ; then
    httpd_user="apache"
fi

echo "Site root is $site_root, httpd user is $httpd_user"

# disable sudo-ing
sudo_cmd=""
if [ "$1" == "--sudo" ] ; then
    sudo_cmd="sudo"
fi

target_db="$site_root/$content_dir/ank/fizlesh.sqlite3"
$sudo_cmd cp $target_db .

echo "Run merger v2.7..."
$sudo_cmd cp settings2.8.php settings.php
$sudo_cmd sed -i -e "s/@@CONTENT@/$content_dir/" settings.php
$sudo_cmd php merger-v2.7-to-v2.8.php
$sudo_cmd cp fizlesh.sqlite3 $target_db

echo "Setting user rights back"
$sudo_cmd chown -R $httpd_user:$httpd_user "$site_root"
