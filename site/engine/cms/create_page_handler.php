<?php

/**
  * @return true on success, error message on failure
  **/

function xcms_create_page()
{
    global $SETTINGS, $pageid;

    $loc_name = xcms_get_key_or($_POST, "create-name");
    if (!xcms_check_page_id($loc_name, true))
        return "Недопустимый физический путь страницы. ";

    $alias = xcms_get_key_or($_POST, "alias");
    if (!xcms_check_page_alias($alias))
        return "Недопустимый alias страницы. ";

    if (@$_POST["global"])
        $dir = xcms_get_page_path($loc_name);
    else
        $dir = xcms_get_page_path("$pageid/$loc_name");

    $page_type = xcms_get_key_or($_POST, "create-pagetype");

    @mkdir($dir);
    $info = array();
    $info["owner"] = xcms_user()->login();
    $info["type"] = $page_type;
    $info["header"] = xcms_get_key_or($_POST, "header");
    $info["alias"] = $alias;

    // set view/edit rights
    // creator always has access
    $info["view"] = xcms_user()->login();
    $info["edit"] = xcms_user()->login();
    xcms_acl_from_post($info);

    if (@$_POST["menu-title"])
        $info["menu-title"] = $_POST["menu-title"];
    xcms_set_key_from_checkbox($info, "menu-hidden", @$_POST["menu-hidden"]);

    if (file_exists("{$SETTINGS["engine_dir"]}cms/$page_type/install.php"))
    {
        $opageid = $pageid;
        if (@$_POST["global"])
            $pageid = $loc_name;
        else
            $pageid = "$pageid/$loc_name";
        include("{$SETTINGS["engine_dir"]}cms/$page_type/install.php");
        $pageid = $opageid;
    }
    xcms_save_list("$dir/info", $info);
    xcmst_rebuild_aliases_and_rewrite();
    foreach ($_POST as $key => $value)
        unset($_POST[$key]);

    return true;
}
