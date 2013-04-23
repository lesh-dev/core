#!/usr/bin/env bash
su apache -c "php tools/xcms_console_tools/xcms.php 'basedir=/srv/www/production' deliver-notifications 'mail-group=reg'"
