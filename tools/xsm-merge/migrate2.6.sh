#!/usr/bin/env bash

set -xe

uid="$(id -u)"
if [ "$1" != "--sudo" ] && [ "$uid" != "0" ] ; then
    echo "Migration should be run under root user"
    exit 1
fi

# Migration script to 2.6 site version
# Place this script into $SITE_ROOT/migrate2.6/ folder

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

news_path="$site_root/$content_dir/cms/pages/z01News"
if grep "owner:" "$news_path/2007.02.16-raboty-na-sayte/info"; then
    echo "Migration is already done"
    exit 1
fi

# disable sudo-ing
sudo_cmd=""
if [ "$1" == "--sudo" ] ; then
    sudo_cmd="sudo"
fi

target_db="$site_root/$content_dir/ank/fizlesh.sqlite3"
$sudo_cmd cp $target_db .

$sudo_cmd cp settings2.6.php settings.php
$sudo_cmd sed -i -e "s/@@CONTENT@/$content_dir/" settings.php

back_path="$news_path.backup"
$sudo_cmd cp -r "$news_path" "$back_path"
$sudo_cmd bash -xe <<EOF
    ls -1 -d $news_path/* | /bin/grep '20' > news-list.txt
EOF
$sudo_cmd php contlist-to-2.6.php news-list.txt
echo "Conversion done"

echo "Removing news backup"
$sudo_cmd rm -rf "$back_path"

echo "Setting user rights back"
$sudo_cmd chown -R $httpd_user:$httpd_user "$site_root"
