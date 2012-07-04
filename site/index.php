<?php
    if (file_exists("install.php"))
    {
        header("Location: install.php");
    }
    header("Content-Type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');
    include ("settings.php");
    include ("$engine_dir/sys/settings.php");
    include ("$engine_dir/sys/logger.php");
    include ("$engine_dir/sys/compiler.php");
    include ("$engine_dir/sys/tag.php");
    include ("$engine_dir/sys/mailer.php");
    include ("$engine_dir/sys/resample.php");

    $main_ref_file = "";
    $main_ref_name = "";
    xcms_main();
    compile($main_ref_file, $main_ref_name);
    include($main_ref_name);
?>
