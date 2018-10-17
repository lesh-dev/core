<?php

global $SETTINGS;
global $content_dir;
$content_dir = "content/";
global $design_dir;
$design_dir = "fizlesh.ru-design/";
global $engine_dir;
$engine_dir = "engine/";
global $xengine_dir;
$xengine_dir = "xengine/";
global $engine_pub;
$engine_pub = "engine_public/";
global $web_prefix;
$web_prefix = "";
$mailer_enabled = false;

require_once("${xengine_dir}sys/db.php");

$SETTINGS['content_time_roundup'] = 100;
$SETTINGS['auth_vk_id'] = '';
$SETTINGS['auth_vk_rights'] = 'notify,offline';

global $meta_site_name;
$meta_site_name = 'fizlesh.local';
global $meta_site_url;
$meta_site_url = 'http://fizlesh.local/';
global $meta_site_log_path;
$meta_site_log_path = '/var/log/xcms/fizlesh.local-engine.log';
global $meta_site_mail;
$meta_site_mail = 'support@fizlesh.local';

$SETTINGS[XDB_DB_TYPE] = XDB_DB_TYPE_SQLITE3;
$SETTINGS[XDB_DB_NAME] = 'ank/fizlesh.sqlite3';

// nextgen: postgres
// $SETTINGS[XDB_DB_TYPE] = XDB_DB_TYPE_PG;
// $SETTINGS[XDB_DB_NAME] = "host=localhost user=lesh password=123 dbname=lesh";
