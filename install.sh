#!/usr/bin/env bash

# Deployment script.
# Contains configuration for all deploy places

. deploy-tools/installer/installer.sh

function xcms_install_version_file() {
    if [ "$mode" = "production" ] ; then
        sudo cp -a version $root/
    else
        version="$(cat version)-$(xcms_git_version)-local"
        print_message "Set version: $version"
        sudo bash -e <<EOF
echo "$version" > $root/version
echo "version: $version" > $root/INFO
EOF
    fi
}

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

print_message "Mode: '$mode'"
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
        content_dir="/srv/www/fizlesh.ru/content-fizlesh.ru"
    else
        print_error "Invalid mode '$mode'. Specify it, please"
        exit 1
    fi
fi

sudo mkdir -p $root
sudo cp -a ./site/* $root/

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
    tmp_db_path=""
    if [ "$mode" = "default" ] ; then
        # in default mode we back up database
        db_path="$root/content/ank/fizlesh.sqlite3"
        if [ -e $db_path ] ; then
            tmp_db_path=$(mktemp fizlesh.XXXXXXXX)
            print_message "Database $db_path backed up"
            cp $db_path $tmp_db_path
        fi
    fi
    print_message "Non-production mode, removing entire content directory"
    sudo rm -rf $root/content
    print_message "Copying test content"
    sudo cp -r $content_dir/content $root/

    if [ "$mode" = "default" ] ; then
        # restore database backed up
        if [ -n "$tmp_db_path" ] ; then
            cp $tmp_db_path $db_path
            print_message "Database $db_path restored from backup"
            rm -f $tmp_db_path
        fi
    fi

    cp $root/settings.local.php $root/settings.php

    if [ -e $root/content/auth/usr/root.user ] ; then
        print_message "Install users with default passwords"
        sudo cp -f $verbose ./tools/xcms_console_tools/*.user $root/content/auth/usr/
    else
        print_error "User 'root' was not found, password change skipped"
    fi
fi

print_message "Clearing cache"
sudo rm -rf $root/.prec/*

print_message "Creating cache directory"
sudo mkdir -p $root/.prec
sudo chmod 777 $root/.prec

sudo chown -R $www_user $root

target_site="fizlesh.local"
if [ "$mode" = "production" ] ; then
    target_site="fizlesh.ru"
elif [ "$mode" = "testing" ] ; then
    target_site="test.fizlesh.ru"
fi

print_message "Rebuilding aliases..."
curl "http://$target_site/?ref=rebuild_aliases"

if ! [ "$mode" = "production" ] ; then
    print_message "Clear notifications and prepare mailer test configuration..."
    curl "http://$target_site/?ref=prepare_mailer_in_testing"
fi

xcms_install_version_file

# version css files after installation
xcms_version_css "$root" "engine_public"
xcms_version_css "$root" "fizlesh.ru-design"
xcms_version_css "$root" "lesh.org.ru-design"

set +x

print_message "$program_name was successfully deployed to '$root' in mode '$mode'"
