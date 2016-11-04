#!/usr/bin/php
<?php
    function xcms_console_main($args, $params)
    {
        if (count($args) == 0)
        {
            throw new Exception("Usage: xcms.php <command> [args]");
        }

        $command = $args[0];
        if ($command == "useradd")
            xcms_console_create_user($params);
        elseif ($command == "deliver-notifications")
        {
            $mail_group = $params["mail-group"];
            xcms_deliver_notifications($mail_group);
        }
        elseif ($command == "xsm-ank-reminder")
        {
            xsm_ank_reminder();
        }
        else
        {
            throw new Exception("Unknown command: '$command'");
        }
    }

    try
    {

        $params = array();
        $params["basedir"] = ".";
        $args = array();
        foreach ($_SERVER["argv"] as $i => $cmd)
        {
            if ($i == 0) continue;
            if (strpos($cmd, '=') !== false)
            {
                $arr = explode('=', $cmd, 2);
                $value = $arr[1];
                if (substr($value, 0, 1) == "'")
                    $value = substr($value, 1, strlen($value) - 2);
                $params[$arr[0]] = $value;
            }
            else
                $args[] = $cmd;
        }

        $basedir = $params["basedir"];
        if (!chdir($basedir))
            throw new Exception("Can't change directory to basedir '$basedir'. ");
        if (!file_exists("index.php"))
            throw new Exception("No index.php found. ");
        if (file_exists("install.php") && filesize("install.php") > 0)
            throw new Exception("Installer detected, this installation is not configured yet. ");
        if (!file_exists("settings.php"))
            throw new Exception("No 'settings.php' detected, this installation is not configured yet. ");

        session_start();
        header("Content-Type: text/html; charset=utf-8");
        date_default_timezone_set('Europe/Moscow');
        require_once ("settings.php");
        require_once ("$engine_dir/sys/settings.php");
        require_once ("$engine_dir/sys/string.php");
        require_once ("$engine_dir/sys/util.php");
        require_once ("$engine_dir/sys/tag.php");
        require_once ("$engine_dir/sys/auth.php");
        require_once ("$engine_dir/sys/logger.php");
        require_once ("$engine_dir/sys/compiler.php");
        require_once ("$engine_dir/sys/db.php");
        require_once ("$engine_dir/sys/mailer.php");
        require_once ("$engine_dir/xsm/reminder.php");

        $main_ref_file = "";
        $main_ref_name = "";
        xcms_main();
        xcms_compile($main_ref_file, $main_ref_name);
        xcms_console_main($args, $params);
    }
    catch (Exception $e)
    {
        echo "ERROR: ".$e->getMessage()."\n";
        exit(1);
    }
?>
