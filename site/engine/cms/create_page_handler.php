<?php

/**
  * Creates page using data in $_POST (page creation handler).
  * @return dict("output", "error")
  * "error" can be either `false` or error message.
  **/

function xcms_create_page()
{
    global $SETTINGS, $pageid;
    $result = array(
        "error" => false,
        "output" => "",
    );

    $loc_name = xcms_get_key_or($_POST, "create-name");
    if (!xcms_check_page_id($loc_name, true))
    {
        $result["error"] = "Недопустимый физический путь страницы. ";
        return $result;
    }

    $alias = xcms_get_key_or($_POST, "alias");
    if (!xcms_check_page_alias($alias))
    {
        $result["error"] = "Недопустимый alias страницы. ";
        return $result;
    }

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

    if (!xcms_save_list("$dir/info", $info))
    {
        $result["error"] = "Cannot save INFO '$dir/info'. ";
        return $result;
    }
    $rebuild_result = xcms_rebuild_aliases_and_rewrite();
    // append output
    $result["output"] .= $rebuild_result["output"];

    if ($rebuild_result["error"] !== false)
        return $rebuild_result;

    foreach ($_POST as $key => $value)
        unset($_POST[$key]);

    return $rebuild_result;
}
