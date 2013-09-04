<?php
    /**
      * News to contlist migration script (2.3 to 2.4)
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
        xcms_log(XLOG_INFO, "Converting $file");
        global $dir_name;
        $dir_name = dirname($file);
        $ts = str_replace(".news", "", $file);
        $ts = (integer)$ts;

        $date = date('Y.m.d', $ts);
        $glob_dir = "$dir_name/$date";
        $dir_list = glob("./$glob_dir-*", GLOB_ONLYDIR);
        //print_r($dir_list);
        $count = count($dir_list);
        if ($count > 0)
            print_r("!!! More news !!!\n");
        $item_id = "$date-$count";

        $contents = file_get_contents($file);
        $r = array();
        preg_match("/newstitle\".[0-9.]+(.*?)</s", $contents, $r);
        $title = "";
        $suffix = "";
        if ($r)
        {
            $title = trim($r[1]);
            $title_tr = strtr(strtolower(xcms_transliterate($title)), " _/", "---");
            $title_tr = preg_replace("/[^0-9a-zA-Z-]/", "", $title_tr);
            $title_tr = preg_replace("/[-]{2,}/", "-", $title_tr);
            $title_tr = substr($title_tr, 0, 50);
            $suffix = "-$title_tr";
        }
        $folder = "$item_id$suffix";
        mkdir("$dir_name/$folder", 0755, true);
        xcms_log(XLOG_INFO, "$folder");
        xcms_write("$dir_name/$folder/content", $contents);
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
        xcms_write("$dir_name/$folder/info", $info_contents);
    }

$info_contents_root =
"owner:root
type:contlist
view:#all
header:Новости
subheader:
edit:#editor
menu-title:Новости
menu-hidden:
menu-auth-only:
";

    if ($argc < 2)
        die ("Usage: ".$argv[0]." <news-list>");

    $list = file($argv[1]);
    foreach ($list as $name)
        xconv_convert_news_file(trim($name));
    xcms_write("$dir_name/info", $info_contents_root);
?>
