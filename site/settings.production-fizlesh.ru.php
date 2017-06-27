<?php
    global $SETTINGS;
    global $content_dir;
    $content_dir = "fizlesh.ru-content/";
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
    $mailer_enabled = true;
    $SETTINGS['content_time_roundup'] = 100;

?><?php
    $SETTINGS['auth_vk_id'] = '';
    $SETTINGS['auth_vk_rights'] = 'notify,offline';
?><?php
/* This block was inserted by installer -- sitemeta.php.
You may edit it, but it can be regenerated. */
    global $meta_site_name;
    $meta_site_name = 'ФизЛЭШ';
    global $meta_site_url;
    $meta_site_url = 'http://fizlesh.ru/';
    global $meta_site_log_path;
    $meta_site_log_path = '/var/log/xcms/fizlesh.local-engine.log';
    global $meta_site_mail;
    $meta_site_mail = 'support@fizlesh.ru';
/* --- */
?><?php
/* This block was inserted by installer -- xsm.php.
You may edit it, but it can be regenerated. */
    $SETTINGS['xsm_db_name'] = 'ank/fizlesh.sqlite3';
/* --- */
?>
