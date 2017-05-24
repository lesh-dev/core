#!/usr/bin/env bash

# Deployment script.
# Contains configuration for all deploy places

program_name="FizLesh"

if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]] ; then
    echo "$program_name deployment script"
    echo "Usage: $0 <mode>"
    echo
    echo "    <mode>      (empty)|production|testing"
    exit 0
fi

set -xe

mode="$1"
if [ -z "$mode" ] ; then
    mode="default"
fi

unalias grep 2>/dev/null || true

host="$( hostname )"
root="/var/www/html"
www_user="www-data:www-data"
content_dir="../content-fizlesh.ru"

if echo $host | grep -q lambda ; then
    root="/var/www/vhosts/fizlesh.ru"
elif echo $host | grep -q blackbox ; then
    root="/var/www/vhosts/fizlesh.ru"
elif echo $host | grep -q fizlesh ; then
    if [ "$mode" = "production" ] ; then
        root="/srv/www/fizlesh.ru/production"
        content_dir="/srv/www/fizlesh.ru/content-fizlesh.ru"
    elif [ "$mode" = "testing" ] ; then
        root="/srv/www/fizlesh.ru/testing"
    else
        echo "Invalid mode '$mode'. Specify it, please"
        exit 1
    fi
fi
sudo mkdir -p $root
sudo cp -a ./site/* $root/
# TODO: version file: site/VERSION or <root>/version ?
# sudo cp version $root/
#sudo mkdir -p $root/data
# sudo chmod -R 777 $root/data

sudo chown -R $www_user $root
sudo rm -f $root/content
if [ "$mode" = "production" ] ; then
    # in production we just use kosher content and set symlink to it
    sudo ln -sf $content_dir/content $root/
else
    # in default/testing mode we clone content from somewhere
    sudo cp -r $content_dir/content $root/
fi

set +x

echo "$program_name was successfully deployed to '$root' in mode '$mode'"
