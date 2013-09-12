<?php
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/unittest.php");
    require_once("${engine_dir}sys/util.php");
    require_once("${engine_dir}sys/auth.php");
    require_once("${engine_dir}sys/diff/diff-utils.php");

    header("Content-Type: text/html; charset=utf-8");

    xut_initialize();

    // put your unit test function call here
    xcms_string_unit_test();
    xcms_keyvalue_unit_test();
    xcms_finediff_unit_test();
    XcmsUser::unit_test();

    xut_finalize();
?>
