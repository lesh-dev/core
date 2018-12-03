<?php

session_set_cookie_params(365 * 24 * 3600); // 2 weeks
$session_result = @session_start();
header("Content-Type: text/html; charset=utf-8");
date_default_timezone_set('Europe/Moscow');

if (!file_exists("settings.php")) {?>
    <html>
        <head>
            <title>XCMS Configuration Error</title>
        </head>
        <body>
            <h1>XCMS Configuration Error</h1>
            <p>Cannot find configuration (<tt>settings.php</tt>). You should
            create it by hands using sample configuration.</p>
        </body>
    </html><?php
    die();
}
require_once("settings.php");

require_once("${full_xengine_dir}sys/settings.php");
require_once("${full_xengine_dir}sys/string.php");
require_once("${full_xengine_dir}sys/tag.php");
require_once("${full_xengine_dir}sys/cms.php");
require_once("${full_xengine_dir}sys/file.php");
require_once("${full_xengine_dir}sys/util.php");
require_once("${full_xengine_dir}sys/unittest.php");
require_once("${full_xengine_dir}sys/auth.php");
require_once("${full_xengine_dir}sys/logger.php");
require_once("${full_xengine_dir}sys/attachment.php");
require_once("${full_xengine_dir}sys/compiler.php");
require_once("${full_xengine_dir}sys/registry.php");
require_once("${full_xengine_dir}sys/mailer.php");
require_once("${full_xengine_dir}sys/resample.php");
require_once("${full_xengine_dir}sys/controls.php");

# old engine parts
require_once("${full_engine_dir}cms/alias.php");

if (!$session_result) {
    xcms_log(XLOG_ERROR, "[SESSION] Session start failed");
}

$main_ref_file = "";
$main_ref_name = "";
xcms_main();
xcms_compile($main_ref_file, $main_ref_name);
try {
    include($main_ref_name);
} catch (Exception $e) {
    xcms_main("exception");
    xcms_compile($main_ref_file, $main_ref_name);
    $Exception = $e;
    include($main_ref_name);
}
