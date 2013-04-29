#!/usr/bin/env bash
XCMS_HOME="/srv/www/production"
su www-data -c "php /srv/tools/git-working-copy/tools/xcms_console_tools/xcms.php 'basedir=$XCMS_HOME' deliver-notifications 'mail-group=reg'"
sleep 1m
su www-data -c "php /srv/tools/git-working-copy/tools/xcms_console_tools/xcms.php 'basedir=$XCMS_HOME' deliver-notifications 'mail-group=content-change'"
