<?php
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${xengine_dir}sys/settings.php");
    require_once("${xengine_dir}sys/file.php");
    require_once("${xengine_dir}sys/unittest.php");
    require_once("${xengine_dir}sys/util.php");
    require_once("${xengine_dir}sys/db.php");
    require_once("${xengine_dir}sys/controls.php");
    require_once("${xengine_dir}sys/auth.php");
    require_once("${xengine_dir}sys/diff/diff-utils.php");
    require_once("${engine_dir}cms/ank/format.php");
    require_once("${engine_dir}cms/ank/ank-proc.php");
    require_once("${engine_dir}cms/ank/field-desc.php");

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
    xdb_unit_test();
    xcms_util_unit_test();
    xcms_string_unit_test();
    xcms_sys_controls_unit_test();
    xcms_keyvalue_unit_test();
    xcms_finediff_unit_test();
    xsm_ank_format_unit_test();
    xsm_ank_proc_unit_test();
    xsm_field_desc_unit_test();
    XcmsUser::unit_test();

    xut_finalize();
?></body></html>