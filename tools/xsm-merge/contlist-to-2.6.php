<?php
    /**
      * Contlist migration script (2.5 to 2.6)
      **/
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/logger.php");
    require_once("${engine_dir}sys/string.php");
    header("Content-Type: text/html; charset=utf-8");

    function xconv_convert_news_file($file)
    {
        xcms_log(XLOG_INFO, "Converting item $file");
        $content_name = "$file/content";
        $info_name = "$file/info";

        $contents = file_get_contents($file);
        $r = array();
        preg_match("/newstitle\".([0-9.]+)(.*?)</s", $contents, $r);
        $title = "";
        $date = "";
        if ($r)
        {
            $date = substr($r[1], 0, 8);
            $title = trim($r[2]);
        }
        echo "$date $title";
        /*$folder = "$item_id$suffix";
        mkdir("$dir_name/$folder", 0755, true);
        xcms_log(XLOG_INFO, "$folder");
        if (!xcms_write("$dir_name/$folder/content", $contents))
            die("Migration failed: cannot write content");
        xcms_log(XLOG_INFO, "Write content to $dir_name/$folder/content");

        $info_contents =
"type:content
subheader:
menu-title:
view:#all
edit:#editor
alias:news/$item_id$suffix
menu-title:$title
menu-hidden:yes
menu-locked:yes
";
        if (!xcms_write("$dir_name/$folder/info", $info_contents))
            die("Migration failed: cannot write info");
        // remove old news file
        unlink($file);
        */
    }

    if ($argc < 2)
        die ("Usage: ".$argv[0]." <contlist-list>");

    $list = file($argv[1]);
    foreach ($list as $name)
        xconv_convert_contlist_item(trim($name));
?>
