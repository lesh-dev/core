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
        mkdir("new-news/$item_id", 0755, true);
        xcms_write("new-news/$item_id/content", $contents);
        print_r("  :Write to new-news/$item_id/content\n");
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
            print_r("  :$title\n");
            print_r("  :$title_tr\n");
            $suffix = "-$title_tr";
        }

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

    }

    if ($argc < 2)
        die ("Usage: ".$argv[0]." <news-list>");

    $list = file($argv[1]);
    foreach ($list as $name)
    {
        xconv_convert_one(trim($name));
    }
?>
