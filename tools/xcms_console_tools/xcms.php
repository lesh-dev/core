#!/usr/bin/php
<?php
    function xcms_console_main($args, $params)
    {
        $command = $args[0];
        if ($command == "useradd")
            xcms_console_create_user($params);
        elseif ($command == "deliver-notifications")
        {
            $mail_group = $params["mail-group"];
            xcms_deliver_notifications($mail_group);
        }
    }

    $params = array();
    $params["basedir"] = ".";
    $args = array();
    foreach ($_SERVER["argv"] as $i=>$cmd)
    {
        if ($i == 0) continue;
        if (strpos($cmd, EXP_EQ) !== false)
        {
            $arr = explode(EXP_EQ, $cmd, 2);
            $params[$arr[0]] = $arr[1];
        }
        else
            $args[] = $cmd;
    }

    $basedir = $params["basedir"];
    if (!chdir($basedir))
        throw new Exception("Can't change directory to basedir. ");
    if (!file_exists("index.php"))
        throw new Exception("No index.php found. ");
    if (file_exists("install.php"))
        throw new Exception("Installer detected, this installation is not configured yet. ");
    if (!file_exists("settings.php"))
        throw new Exception("No 'settings.php' detected, this installation is not configured yet. ");

    session_start();
    header("Content-Type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');
    require_once ("settings.php");
    require_once ("$engine_dir/sys/settings.php");
    require_once ("$engine_dir/sys/string.php");
    require_once ("$engine_dir/sys/tag.php");
    require_once ("$engine_dir/sys/auth.php");
    require_once ("$engine_dir/sys/logger.php");
    require_once ("$engine_dir/sys/compiler.php");
    require_once ("$engine_dir/sys/db.php");
    require_once ("$engine_dir/sys/mailer.php");

    $main_ref_file = "";
    $main_ref_name = "";
    xcms_main();
    xcms_compile($main_ref_file, $main_ref_name);
    xcms_console_main($args, $params);
?>
