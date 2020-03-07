<?php
global $SETTINGS;

// This, in particular, disables some unauthorized handlers
$SETTINGS["production"] = true;

global $content_dir;
$content_dir = "content/";

global $design_dir;
$design_dir = "lesh.org.ru-design/";

global $engine_dir;
$engine_dir = "engine/";

global $xengine_dir;
$xengine_dir = "xengine/";

global $engine_pub;
$engine_pub = "engine_public/";

global $web_prefix;
$web_prefix = "";

$mailer_enabled = true;

// DO NOT EDIT THIS PART
// UNLESS YOU UNDERSTAND
// WHAT ARE YOU DOING!
global $full_web_prefix;
$full_web_prefix = "${_SERVER["DOCUMENT_ROOT"]}/${web_prefix}";

global $full_xengine_dir;
$full_xengine_dir = "${full_web_prefix}${xengine_dir}";

global $full_engine_dir;
$full_engine_dir = "${full_web_prefix}${engine_dir}";

require_once("${full_xengine_dir}sys/db_const.php");
// END OF IMMUTABLE PART

$SETTINGS['content_time_roundup'] = 100;
$SETTINGS['auth_vk_id'] = '';
$SETTINGS['auth_vk_rights'] = 'notify,offline';

global $meta_site_name;
$meta_site_name = 'ФизЛЭШ';

global $meta_site_url;
$meta_site_url = 'http://lesh.org.ru/';

global $meta_site_log_path;
$meta_site_log_path = '/var/log/xcms/lesh.org.ru-engine.log';

global $meta_site_mail;
$meta_site_mail = 'support@fizlesh.ru';

// same XSM database as for fizlesh.ru
$SETTINGS[XDB_DB_TYPE] = XDB_DB_TYPE_PG;
$SETTINGS[XDB_DB_NAME] = "host=localhost user=lesh password=fizlesh dbname=lesh";
