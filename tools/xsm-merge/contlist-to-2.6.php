<?php
    /**
      * Contlist migration script (2.5 to 2.6)
      **/
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${xengine_dir}sys/settings.php");
    require_once("${xengine_dir}sys/file.php");
    require_once("${xengine_dir}sys/util.php");
    require_once("${xengine_dir}sys/logger.php");
    require_once("${xengine_dir}sys/string.php");
    require_once("${xengine_dir}sys/tag.php");
    header("Content-Type: text/html; charset=utf-8");

    $A = array();

    function parse_signature($sig)
    {
        if (strpos($sig, "Дима") !== false)
            return "vdm";
        if (strpos($sig, "vdm") !== false)
            return "vdm";
        if (strpos($sig, "Миша") !== false)
            return "mvel";
        if (strpos($sig, "Кузн") !== false)
            return "mvel";
        if (strpos($sig, "Serge") !== false)
            return "serge";
        if (strpos($sig, "rsen") !== false)
            return "arseniy";
        if (strpos($sig, "Демар") !== false)
            return "dimchik";
        if (strpos($sig, "dimch") !== false)
            return "dimchik";
        if (strpos($sig, "demar") !== false)
            return "dimchik";
        if (strpos($sig, "Дара") !== false)
            return "dara";
        if (strpos($sig, "Жигул") !== false)
            return "alena";
        if (strpos($sig, "Лилиен") !== false)
            return "ivan_lilienberg";
        if (strpos($sig, "Trous") !== false)
            return "doctor";
        return $sig;
    }

    function xconv_convert_contlist_item($file)
    {
        xcms_log(XLOG_INFO, "Converting item $file");
        $content_name = "$file/content";
        $info_name = "$file/info";

        $contents = file_get_contents($content_name);
        $r = array();
        preg_match("/newstitle\".([0-9.]+)(.*?)</s", $contents, $r);
        $title = "";
        $date = "";
        if ($r)
        {
            $date = substr($r[1], 0, 8);
            $date = '20'.substr($date, 6, 2).'-'.substr($date, 3, 2).'-'.substr($date, 0, 2);
            $title = trim($r[2]);
        }

        $r = array();
        preg_match(":signature\".*?>(.*?)</div:s", $contents, $r);
        $signature = "";
        if ($r)
        {
            $signature = trim($r[1]);
        }
        else
        {
            preg_match(":align.*?>(.*?)</div:", $contents, $r);
            if ($r)
            {
                $signature = trim($r[1]);
            }
            else
            {
                if ($date == "2011-07-23")
                    $signature = "serge";
                else
                {
                    die("Cannot match owner in $contents");
                }
            }
        }
        if (!$signature)
            die("EMPTY $contents");
        $signature = parse_signature($signature);
        if ($signature == "root")
            $signature = "doctor";

        global $A;
        $A[$signature] = $signature;

        $r = array();
        preg_match(":(<p.*</p>):s", $contents, $r);
        $news_text = "";
        if ($r)
        {
            $news_text = $r[1];
        }
        else
        {
            preg_match(":</div>(.*?)<div:s", $contents, $r);
            if ($r)
            {
                $news_text = $r[1];
            }
            else
            {
                if ($date == "2011-07-23")
                {
                    preg_match(":</div>(.*):s", $contents, $r);
                    if ($r)
                    {
                        $news_text = $r[1];
                    }
                    else
                        die("Cannot extract SERGE content: $contents");
                }
                else
                    die("Cannot extract content: $contents");
            }
        }

        $ts = strtotime($date);

        $info = xcms_get_list($info_name);
        $info["type"] = "content";
        unset($info["subheader"]);
        $info["header"] = $title;
        $info["menu-title"] = $title;
        $info["owner"] = $signature;
        $info["datetime-created"] = xcms_datetime($ts);
        $info["timestamp-created"] = $ts;

        echo "$date $ts $title\n$news_text\n\n";
        //print_r($info);
        xcms_write($content_name, $news_text);
        xcms_save_list($info_name, $info);
    }

    if ($argc < 2)
        die ("Usage: ".$argv[0]." <contlist-list>");

    $list = file($argv[1]);
    foreach ($list as $name)
        xconv_convert_contlist_item(trim($name));
    print_r($A);
?>
