<?php

/**
  * Checks whether page alias is valid
  * @return true if alias is valid, false otherwise
  **/
function xcms_check_page_alias($alias)
{
    // everything should be replaced if OK
    $bad = preg_replace("#[a-z/A-Z.0-9_-]+#i", "", $alias);
    return xu_empty($bad);
}

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
    // no aliases is not an error
    $aliases_name = xcms_get_aliases_file_name();
    if (!file_exists($aliases_name))
        return array();
    return xcms_get_list($aliases_name);
}

/**
  * Writes map of alias->page_id to content
  **/
function xcms_save_aliases($list)
{
    xcms_save_list(xcms_get_aliases_file_name(), $list);
}

/**
  * Return page alias by page id
  **/
function xcms_get_page_alias($page_id)
{
    $aliases = xcms_get_aliases();
    foreach ($aliases as $alias => $path)
    {
        if ($path == $page_id)
            return $alias;
    }
    return "";
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
        if (xu_not_empty($cur_alias))
        {
            if (array_key_exists($cur_alias, $aliases))
            {
                throw new Exception("Duplicate aliases for pages '$info_fn' and '".
                    $aliases[$cur_alias]."'. ");
            }
            $aliases[$cur_alias] = $page_id;
        }
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
    $root = "{$SETTINGS["content_dir"]}cms/pages";
    $aliases = array();
    xcms_collect_aliases_int($aliases, $root, strlen($root));
    return $aliases;
}

/**
 * Rebuilds aliases
 * @return true on success, error message on failure.
 **/
function xcms_rebuild_aliases()
{
    try
    {
        $aliases = xcms_collect_aliases();
    }
    catch (Exception $err)
    {
        return $err->getMessage();
    }
    xcms_save_aliases($aliases);
    return true;
}

?>