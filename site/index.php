<?php
    session_set_cookie_params(14 * 24 * 3600); // 2 weeks
    $session_result = @session_start();
    if (file_exists("install.php") && filesize("install.php") > 0)
    {
        header("Location: install.php");
        exit(0);
    }
    header("Content-Type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');
    require_once ("settings.php");
    require_once ("$engine_dir/sys/settings.php");
    require_once ("$engine_dir/sys/string.php");
    require_once ("$engine_dir/sys/tag.php");
    require_once ("$engine_dir/sys/cms.php");
    require_once ("$engine_dir/sys/file.php");
    require_once ("$engine_dir/sys/util.php");
    require_once ("$engine_dir/sys/unittest.php");
    require_once ("$engine_dir/sys/auth.php");
    require_once ("$engine_dir/sys/logger.php");
    require_once ("$engine_dir/sys/compiler.php");
    require_once ("$engine_dir/sys/mailer.php");
    require_once ("$engine_dir/sys/resample.php");
    if (!$session_result)
        xcms_log("Session start failed");

    $main_ref_file = "";
    $main_ref_name = "";
    xcms_main();
    xcms_compile($main_ref_file, $main_ref_name);
    try
    {
        include($main_ref_name);
    }
    catch(Exception $e)
    {
        xcms_main("exception");
        xcms_compile($main_ref_file, $main_ref_name);
        $Exception = $e;
        include($main_ref_name);
    }
?>