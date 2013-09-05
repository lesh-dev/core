#!/usr/bin/env bash

set -xe

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

target_db="$site_root/$content_dir/ank/fizlesh.sqlite3"
sudo cp $target_db .

echo "Run merger v2.3..."
sudo cp settings2.4.php settings.php
sudo sed -i -e "s/@@CONTENT@/$content_dir/" settings.php
sudo php merger-v2.3-to-v2.4.php
sudo cp fizlesh.sqlite3 $target_db

news_path="$site_root/$content_dir/cms/pages/z01News"
back_path="$news_path.backup"
sudo cp -r "$news_path" "$back_path"
sudo rm -f "$news_path"/*.gz
sudo bash -xe <<EOF
    ls -1 $news_path/*.news > news-list.txt
EOF
sudo bash -xe <<EOF
    # remove old metainfo
    rm -f $news_path/_*
    # remove unused template
    rm -f $news_path/template
EOF
sudo php news-to-contlist2.4.php news-list.txt
echo "Conversion done"

echo "Removing news backup"
sudo rm -rf "$back_path"

echo "Setting user rights back"
sudo chown -R $httpd_user:$httpd_user "$site_root"
