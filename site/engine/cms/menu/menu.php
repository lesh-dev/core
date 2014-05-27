<?php
    function xcms_menu($init_path, $MENUTEMPLATES, $menu_level, $add_href_params, $options, $start_level, $end_level)
    {
        global $SETTINGS, $pageid, $web_prefix;

        $page_prefix = xcms_get_page_root(true);
        $pageiid = str_replace($page_prefix, "", $init_path);
        $aux_class = "";
        $flags = "";
        $page_info = "$init_path/info";
        $text = "";
        // this prevents from loading sub-folders if no info file here
        if (!file_exists($page_info))
            return;

        $INFO = xcms_get_list($page_info);
        $show = xcms_get_key_or($options, "show");
        $view = trim(xcms_get_key_or($INFO, "view"));
        $acl = explode(EXP_SP, $view);
        $access_granted = xu_empty($view) || xcms_check_rights($acl);
        if ($show != "")
        {
            $text = "{unnamed}";
            if (xcms_get_key_or($INFO, "menu-title"))
                $text = htmlspecialchars($INFO["menu-title"]);

            // skip locked items in not-locked mode
            if ($show == "not-locked" && xcms_is_enabled_key($INFO, "menu-locked"))
                return;

            if (xcms_is_enabled_key($INFO, "menu-hidden", false))
            {
                $aux_class .= "menuitem-hidden ";
                $flags .= "H";
            }
            if ($flags)
                $text = "<sup>$flags</sup>$text";
        }
        else
        {
            $text = htmlspecialchars(@$INFO["menu-title"]);
            // don't show unnamed items
            if (!xcms_get_key_or($INFO, "menu-title")) // no title
                return;
            // don't show hidden items
            if (xcms_is_enabled_key($INFO, "menu-hidden", false))
                return;
            if (!$access_granted)
                return;

            $reg_only = true;
            foreach ($acl as $acl_item)
                if ($acl_item == "#all")
                    $reg_only = false;
            if ($reg_only)
                $aux_class .= " menuitem-auth";
        }
        // render menu item
        $html = $MENUTEMPLATES[$menu_level];
        $html = str_replace('<AUXCLASS>', $aux_class, $html);

        if (xcms_get_key_or($options, "devel") || !@$INFO["alias"])
        {
            // if alias not set or in devel mode, always show unaliased menu items
            $html = str_replace("<HREF>", "/$web_prefix?page=$pageiid&amp;$add_href_params", $html);
        }
        else
        {
            $alias = $INFO["alias"];
            $html = str_replace("<HREF>", "/$web_prefix$alias/$add_href_params", $html);
        }
        // text is already escaped here
        $html = str_replace("<TEXT>", $text, $html);

        if ($pageid == $pageiid || strstr($pageid, "$pageiid/"))
            $html = str_replace("<ACTIVE>", "active", $html);
        else
            $html = str_replace("<ACTIVE>", "passive", $html);

        // add icon
        if (file_exists("$init_path/menuicon.gif"))
            $html = str_replace("<!-- PIC -->", "<img src=\"$init_path/menuicon.gif\" />", $html);

        // render current level
        if ($menu_level >= $start_level && $menu_level <= $end_level)
            echo $html;

        // render menu subtree
        $array = glob("$init_path/*", GLOB_ONLYDIR);
        if (xcms_get_key_or($options, "stop"))
            return;
        if (!@$array)
            return;

        foreach ($array as $key=>$value)
        {
            if (!file_exists("$value/info")) continue;
            $without_prefix = str_replace($page_prefix, "", $value);
            if (xcms_get_key_or($options, "show") != "" || strstr($pageid, $without_prefix))
                xcms_menu($value, $MENUTEMPLATES, $menu_level+1, $add_href_params, $options, $start_level, $end_level);
            else
            {
                $new_options = $options;
                $new_options["stop"] = true;
                xcms_menu($value, $MENUTEMPLATES, $menu_level+1, $add_href_params, $new_options, $start_level, $end_level);
            }
        }
    }
?>