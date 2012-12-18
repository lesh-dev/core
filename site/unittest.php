<?php
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/unittest.php");
    require_once("${engine_dir}sys/auth.php");

    header("Content-Type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');

    xut_initialize();

    XcmsUser::unit_test();

    xut_finalize();
?>
