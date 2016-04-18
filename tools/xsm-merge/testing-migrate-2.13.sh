#!/usr/bin/env bash
set -xe

#if [ "`id -u`" != "0" ]; then
#    echo "You're not root to perform migration. "
#fi

mig_ver="2.13"

echo "Migrating test installation..."
cd /srv/tools/git-working-copy/tools/xsm-merge
sudo git pull
SITE_ROOT=/srv/www/fizlesh.ru/testing
sudo cp -v $mig_ver/send_form $SITE_ROOT/content/cms/pages/z022contest/send_form/content
sudo cp -v $mig_ver/anketa $SITE_ROOT/content/cms/pages/z024JoinUs/anketa/content

echo "Testing installation migrate to v$mig_ver completed. "
