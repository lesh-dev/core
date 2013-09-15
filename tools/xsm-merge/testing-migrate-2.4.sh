#!/bin/bash
set -xe

#if [ "`id -u`" != "0" ]; then
#	echo "You're not root to perform migration. "
#fi

echo "Migrating test installation..."
cd /srv/tools/git-working-copy/tools/xsm-merge
sudo git pull
SITE_ROOT=/srv/www/clones/testing
sudo ./migrate-install2.4.sh "$SITE_ROOT"
cd "$SITE_ROOT/migrate2.4/"
sudo ./migrate2.4.sh

cat /srv/www/clones/testing/content/cms/pages/index/content | awk '{if (substr($0, 0, 5)=="<?php") { exit; } else { print $0; } }' > /tmp/new-index-content.txt
echo '<h2>Новости</h2><div style="position: relative"><?php $pageid = "z01News"; include(translate("<! cms/contlist/view !>"));?></div>' >> /tmp/new-index-content.txt
sudo mv /tmp/new-index-content.txt /srv/www/clones/testing/content/cms/pages/index/content
sudo chown www-data:www-data /srv/www/clones/testing/content/cms/pages/index/content

echo "Migration to 2.4 of test installation done. "
