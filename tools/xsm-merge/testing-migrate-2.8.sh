#!/usr/bin/env bash
set -xe

#if [ "`id -u`" != "0" ]; then
#    echo "You're not root to perform migration. "
#fi

mig_ver="2.8"

echo "Migrating test installation..."
cd /srv/tools/git-working-copy/tools/xsm-merge
sudo git pull
SITE_ROOT=/srv/www/fizlesh.ru/testing
sudo ./migrate-install$mig_ver.sh "$SITE_ROOT"
cd "$SITE_ROOT/migrate$mig_ver/"
sudo ./migrate$mig_ver.sh

echo "Testing installation migrate to v$mig_ver completed. "
