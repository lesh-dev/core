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
?>