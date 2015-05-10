#!/usr/bin/env bash

# default value
XCMS_HOME="/srv/www/fizlesh.ru/production"

if [ -n "$1" ] ; then
    XCMS_HOME="$1"
fi

console_cmd="php /srv/tools/git-working-copy/tools/xcms_console_tools/xcms.php"

su www-data -c "$console_cmd 'basedir=$XCMS_HOME' deliver-notifications 'mail-group=reg'"
sleep 1m
su www-data -c "$console_cmd 'basedir=$XCMS_HOME' deliver-notifications 'mail-group=content-change'"
sleep 1m
su www-data -c "$console_cmd 'basedir=$XCMS_HOME' deliver-notifications 'mail-group=ctx'"
sleep 1m
su www-data -c "$console_cmd 'basedir=$XCMS_HOME' xsm-ank-reminder"
