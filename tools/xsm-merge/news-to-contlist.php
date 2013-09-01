<?php
    /**
      * News to contlist migration script (2.3 to 2.4)
      **/

    $engine_dir = "../../site/engine/";
    date_default_timezone_set('Europe/Moscow');
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/string.php");
    header("Content-Type: text/html; charset=utf-8");

    function xconv_convert_one($file)
    {
        print_r("Converting $file\n");
        $ts = str_replace(".news", "", $file);
        $ts = (integer)$ts;

        $date = date('Y.m.d', $ts);
        $glob_dir = "new-news/$date";
        $dir_list = glob("./$glob_dir-*", GLOB_ONLYDIR);
        //print_r($dir_list);
        $count = count($dir_list);
        if ($count > 0)
            print_r("!!! More news !!!\n");
        $item_id = "$date-$count";

        $contents = file_get_contents("news/$file");
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
        mkdir("new-news/$folder", 0755, true);
        print_r("$folder\n");
        xcms_write("new-news/$folder/content", $contents);
        print_r("  :Write to new-news/$folder/content\n");

        $info_contents =
"type:content
subheader:
menu-title:
view:#all
edit:#editor
alias:news/$item_id$suffix
menu-hidden:yes
menu-locked:yes
";
        xcms_write("new-news/$folder/info", $info_contents);
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
        xconv_convert_one(trim($name));
    xcms_write("new-news/info", $info_contents_root);
?>
