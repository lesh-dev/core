#!/usr/bin/env bash

set -xe

uid="$(id -u)"
if [ "$1" != "--sudo" ] && [ "$uid" != "0" ] ; then
    echo "Migration should be run under root user"
    exit 1
fi

# Migration script to 2.4 site version
# Place this script into $SITE_ROOT/migrate2.4/ folder

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
if grep "contlist" "$news_path/info"; then
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

echo "Run merger v2.3..."
$sudo_cmd cp settings2.4.php settings.php
$sudo_cmd sed -i -e "s/@@CONTENT@/$content_dir/" settings.php
$sudo_cmd php merger-v2.3-to-v2.4.php
$sudo_cmd cp fizlesh.sqlite3 $target_db

back_path="$news_path.backup"
$sudo_cmd cp -r "$news_path" "$back_path"
$sudo_cmd rm -f "$news_path"/*.gz
$sudo_cmd bash -xe <<EOF
    ls -1 $news_path/*.news > news-list.txt
EOF
$sudo_cmd bash -xe <<EOF
    # remove old metainfo
    rm -f $news_path/_*
    # remove unused template
    rm -f $news_path/template
EOF
$sudo_cmd php news-to-contlist2.4.php news-list.txt
echo "Conversion done"

echo "Removing news backup"
$sudo_cmd rm -rf "$back_path"

echo "Setting user rights back"
$sudo_cmd chown -R $httpd_user:$httpd_user "$site_root"
