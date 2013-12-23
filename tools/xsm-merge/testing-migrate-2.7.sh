#!/usr/bin/env bash
set -xe

#if [ "`id -u`" != "0" ]; then
#    echo "You're not root to perform migration. "
#fi

echo "Migrating test installation..."
cd /srv/tools/git-working-copy/tools/xsm-merge
sudo git pull
SITE_ROOT=/srv/www/clones/testing
sudo ./migrate-install2.7.sh "$SITE_ROOT"
cd "$SITE_ROOT/migrate2.7/"
sudo ./migrate2.7.sh

echo "Migration to 2.7 of test installation done. "
