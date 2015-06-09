<?php
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/unittest.php");
    require_once("${engine_dir}sys/util.php");
    require_once("${engine_dir}sys/auth.php");
    require_once("${engine_dir}sys/diff/diff-utils.php");
    require_once("${engine_dir}cms/ank/format.php");
    require_once("${engine_dir}cms/ank/ank-proc.php");

    header("Content-Type: text/html; charset=utf-8");
?><!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>XCMS Unit Tests</title>
</head>
<body><?php
    xut_initialize();

    // put your unit test function call here
    xcms_util_unit_test();
    xcms_string_unit_test();
    xcms_keyvalue_unit_test();
    xcms_finediff_unit_test();
    xsm_ank_format_unit_test();
    xsm_ank_proc_unit_test();
    XcmsUser::unit_test();

    xut_finalize();
?></body></html>