<?php
    /**
      * News to contlist migration script (2.3 to 2.4)
      **/
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/unittest.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/util.php");
    require_once("${engine_dir}sys/auth.php");
    header("Content-Type: text/html; charset=utf-8");

    function xconv_convert_one($file)
    {
        print_r("Converting $file");
        $ts = str_replace(".news", "", $file);
        $ts = (integer)$ts;

        $date = date('Y.m.d', $ts);
        $glob_dir = "$date";
        $count = count(glob("./$glob_dir*", GLOB_ONLYDIR));
        $item_id = "$date-$count";
        print_r($item_id);
    }

    global $SETTINGS;
    if ($argc < 2)
        die ("Usage: ".$argv[0]." <news-list>");

    $list = file_get_contents($argv[1]);
    foreach ($list as $name)
    {
        xconv_convert_one(trim($name));
    }
?>
