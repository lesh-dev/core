<?php
    session_start();
    if (file_exists("install.php"))
    {
        header("Location: install.php");
    }
    header("Content-Type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');
    require_once ("settings.php");
    require_once ("$engine_dir/sys/auth.php");
    require_once ("$engine_dir/sys/settings.php");
    require_once ("$engine_dir/sys/logger.php");
    require_once("$engine_dir/sys/compiler.php");
    require_once ("$engine_dir/sys/tag.php");
    require_once ("$engine_dir/sys/mailer.php");
    require_once ("$engine_dir/sys/resample.php");

    $main_ref_file = "";
    $main_ref_name = "";
    xcms_main();
    compile($main_ref_file, $main_ref_name);
    try
    {
        include($main_ref_name);
    }
    catch(Exception $e)
    {
        xcms_main("exception");
        compile($main_ref_file, $main_ref_name);
        $Exception = $e;
        include($main_ref_name);
    }
?>
