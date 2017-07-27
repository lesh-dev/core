#!/usr/bin/env bash

# Deployment script.
# Contains configuration for all deploy places

. deploy-tools/installer/installer.sh

program_name="FizLesh"

if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]] ; then
    echo "$program_name deployment script"
    echo "Usage: $0 <mode>"
    echo
    echo "    <mode>      (empty)|production|testing"
    exit 0
fi

set -e
# TODO(mvel) support verbose mode

mode="$1"
if [ -z "$mode" ] ; then
    mode="default"
fi
verbose=""

unalias grep 2>/dev/null || true

host="$( hostname )"
root="/var/www/vhosts/fizlesh.ru"
www_user="www-data:www-data"
content_dir="../content-fizlesh.ru"

if echo $host | grep -q fizlesh ; then
    if [ "$mode" = "production" ] ; then
        root="/srv/www/fizlesh.ru/production"
        content_dir="/srv/www/fizlesh.ru/content-fizlesh.ru"
    elif [ "$mode" = "testing" ] ; then
        root="/srv/www/fizlesh.ru/testing"
    else
        print_error "Invalid mode '$mode'. Specify it, please"
        exit 1
    fi
fi

sudo mkdir -p $root
sudo cp -a ./site/* $root/
sudo cp -a version $root/

if [ "$mode" = "production" ] ; then
    # in production we just use kosher content and set symlink to it
    if [ -e $root/content ] ; then
        print_message "Unlinking content symlink"
        sudo rm -f $root/content
    fi
    print_message "Setting production content symlink"
    sudo ln -sf $content_dir/content $root/
    # FIXME(mvel): lesh.org.ru install
    cp $root/settings.production-fizlesh.ru.php $root/settings.php
else
    # in default/testing mode we clone content from somewhere
    print_message "Non-production mode, removing entire content directory"
    sudo rm -rf $root/content
    print_message "Copying test content"
    sudo cp -r $content_dir/content $root/
    cp $root/settings.local.php $root/settings.php

    if [ -e $root/content/auth/usr/root.user ] ; then
        print_message "Changing root password to 'root'..."
        # change root password to 'root'
        sudo cp -f $verbose ./tools/xcms_console_tools/root_root_user $root/content/auth/usr/root.user
    else
        print_error "User 'root' was not found, password change skipped"
    fi
fi

print_message "Creating cache directory"
sudo mkdir -p $root/.prec
sudo chmod 777 $root/.prec
sudo chown -R $www_user $root

xcms_version_css "$root" "engine_public"
xcms_version_css "$root" "fizlesh.ru-design"
xcms_version_css "$root" "lesh.org.ru-design"

target_site="fizlesh.local"
if [ "$mode" = "production" ] ; then
    target_site="fizlesh.ru"
fi

if ! [ "$mode" = "production" ] ; then
    print_message "Rebuilding aliases..."
    curl "http://$target_site/?ref=rebuild_aliases"

    print_message "Clear notifications and prepare mailer test configuration..."
    curl "http://$target_site/?ref=prepare_mailer_in_testing"
fi

set +x

print_message "$program_name was successfully deployed to '$root' in mode '$mode'"
