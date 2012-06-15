<?php
    function xcms_menu($initPath, $MENUTEMPLATES, $menuLevel, $addhrefparams, $options, $startLevel, $endLevel)
    {
        global $SETTINGS, $pageid, $web_prefix;

        $page_prefix = "{$SETTINGS["datadir"]}cms/pages/";
        $pageiid = str_replace($page_prefix, "", $initPath);
        $flags = "";
        $page_info = "$initPath/info";
        $text = "";
        if (!file_exists($page_info)) return;
        $INFO = xcms_get_list($page_info);
        if (strstr($options, "+displayall"))
        {
            $text = "{unnamed}";
            if (array_key_exists("menu-title", $INFO))
            {
                if (strlen($INFO["menu-title"]))
                    $text = $INFO["menu-title"];
            }
            if (array_key_exists("menu-locked", $INFO))
                $flags .= "H ";
        }
        else
        {
            $text = @$INFO["menu-title"];
            // don't show unnamed items
            if (!array_key_exists("menu-title", $INFO)) // no title
                return;
            // don't show locked items
            if (array_key_exists("menu-locked", $INFO))
                return;
            // don't show inaccessible menu items
            // TODO: это называлось hidemenu, для удобства пользования
            if (array_key_exists("menu-auth-only", $INFO))
            {
                include(translate("<! auth/lauth {$INFO['view']} !>"));
                // TODO: OMFG global var reading...
                if (!$access)
                    return;
            }
        }
        // render menu item
        $html = $MENUTEMPLATES[$menuLevel];
        if (strstr($options, "+devel"))
        {
            $margin = $menuLevel*10;
            $html = "<div style=\"margin-left: ${margin}pt;\">[<a href=\"<HREF>\">$flags<TEXT></a>]</div>";
            $html = str_replace("<HREF>","/$web_prefix?page=$pageiid&amp;$addhrefparams", $html);
        }
        elseif (@$INFO["alias"])
        {
            $alias = $INFO["alias"];
            $html = str_replace("<HREF>","/$web_prefix$alias/$addhrefparams", $html);
        }
        else
            $html = str_replace("<HREF>","/$web_prefix?page=$pageiid&amp;$addhrefparams", $html);
        $html = str_replace("<TEXT>", htmlspecialchars($text), $html);

        if (strstr($pageid, $pageiid))
            $html = str_replace("<ACTIVE>", "active", $html);
        else
            $html = str_replace("<ACTIVE>", "passive", $html);

        // add icon
        if (file_exists("$initPath/menuicon.gif"))
            $html = str_replace("<!-- PIC -->", "<img src=\"$initPath/menuicon.gif\" />", $html);

        // render current level
        if ($menuLevel >= $startLevel && $menuLevel <= $endLevel)
            echo $html;

        // render menu subtree
        $array = glob("$initPath/*", GLOB_ONLYDIR);
        if (strstr($options, "+hault"))
            return;
        if (!@$array)
            return;

        foreach ($array as $key=>$value)
        {
            if (!file_exists("$value/info")) continue;
            if (strstr($options,"+devel") || strstr($pageid, str_replace($page_prefix, "", $value)))
                xcms_menu($value, $MENUTEMPLATES, $menuLevel+1, $addhrefparams, $options, $startLevel, $endLevel);
            else
                xcms_menu($value, $MENUTEMPLATES, $menuLevel+1, $addhrefparams, "$options+hault", $startLevel, $endLevel);
        }
    }
?>