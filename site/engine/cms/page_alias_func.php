<?php
    /**
      * Returns aliases file name
      **/
    function xcms_get_aliases_file_name()
    {
        global $content_dir;
        return "${content_dir}cms/aliases";
    }

    /**
      * Returns aliases in the key-value format as alias->page_id mapping
      **/
    function xcms_get_aliases()
    {
        return xcms_get_list(xcms_get_aliases_file_name());
    }

    /**
      * Writes map of alias->page_id to content
      **/
    function xcms_save_aliases($list)
    {
        xcms_save_list(xcms_get_aliases_file_name(), $list);
    }

    /**
      * Internal-usage function (@sa xcms_collect_aliases)
      * and should not be invoked directly
      **/
    function xcms_collect_aliases_int(&$aliases, $dir, $root_len)
    {
        $subdirs = glob("$dir/*", GLOB_ONLYDIR);
        $info_fn = "$dir/info";
        if (file_exists($info_fn))
        {
            $cur_info = xcms_get_list($info_fn);
            $page_id = substr($dir, $root_len + 1);
            $cur_alias = xcms_get_key_or($cur_info, "alias");
            if (!empty($cur_alias))
                $aliases[$cur_alias] = $page_id;
        }
        foreach ($subdirs as $subdir)
        {
            xcms_collect_aliases_int($aliases, $subdir, $root_len);
        }
    }

    /**
      * Recursively walks by content directories and builds aliases mapping
      * into the alias->page_id array
      **/
    function xcms_collect_aliases()
    {
        global $SETTINGS;
        $root = "{$SETTINGS["datadir"]}cms/pages";
        $aliases = array();
        xcms_collect_aliases_int($aliases, $root, strlen($root));
        return $aliases;
    }
?>