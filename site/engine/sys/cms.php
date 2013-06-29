<?php
/**
  * TODO: Add pageid regex checking for safety
  **/

/**
  * Retrieve current page content location
  * Assumes @name pageid and @name SETTINGS are defined
  **/
function xcms_get_info_file_name()
{
    global $SETTINGS;
    global $pageid;
    return "{$SETTINGS["datadir"]}cms/pages/$pageid/info";
}

/**
  * Retrieve current page directory
  * Assumes @name pageid and @name SETTINGS are defined
  **/
function xcms_get_page_path()
{
    global $SETTINGS;
    global $pageid;
    return "{$SETTINGS["datadir"]}cms/pages/$pageid";
}

/**
  * Retrieve current page directory
  * Assumes @name pageid and @name SETTINGS are defined
  **/
function xcms_get_page_prefix($need_slash = true)
{
    global $SETTINGS;
    return "{$SETTINGS["datadir"]}cms/pages" . ($need_slash ? "/" : "");
}

/**
  * Retrieve current page directory
  * Assumes @name pageid and @name SETTINGS are defined
  **/
function xcms_get_page_menu_icon()
{
    global $SETTINGS;
    global $pageid;
    return "{$SETTINGS["datadir"]}cms/pages/$pageid/menu-icon.png";
}

function xcms_get_page_content_name($page_id)
{
    global $SETTINGS;
    return "{$SETTINGS["datadir"]}cms/pages/$page_id/content";
}

function xcms_get_template_name($name)
{
    global $SETTINGS;
    return "{$SETTINGS["engine_dir"]}cms/content/$name.template";
}

function xcms_get_templates()
{
    $prefix = "{$SETTINGS["engine_dir"]}cms/content/";
    $ext = ".template";
    $list = glob("$prefix*$ext");
    $name_list = array();
    foreach ($list as $key=>$value)
    {
        $value = str_replace($prefix, "", $value);
        $value = str_replace($ext, "", $value);
        $name_list[] = $value;
    }
}

function xcms_get_page_comments_name()
{
    global $SETTINGS;
    global $pageid;
    return "{$SETTINGS["datadir"]}cms/pages/$pageid/comments";
}

/**
  * Retrieve all subpage ids of given page
  * Assumes @name SETTINGS is defined
  * @return array of page ids
  **/
function xcms_get_subpages($page_id)
{
    global $SETTINGS;
    $path_prefix = "{$SETTINGS["datadir"]}cms/pages/";
    $list = glob("${path_prefix}$page_id/*", GLOB_ONLYDIR);
    $page_ids = array();
    foreach ($list as $subpage_id)
        $page_ids[] = str_replace($path_prefix, "", $subpage_id);
    return $page_ids;
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