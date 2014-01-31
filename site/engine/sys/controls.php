<?php

require_once("${engine_dir}sys/string.php");
require_once("${engine_dir}sys/tag.php");

define('XCMS_FROM_POST', '{{{XCMS_FROM_POST}}}');
define('XCMS_FROM_GET', '{{{XCMS_FROM_GET}}}');
define('XCMS_CHECKBOX_ENABLED', 'enabled');
define('XCMS_CHECKBOX_DISABLED', '');

function xcms_checkbox_enabled($value)
{
    return xu_not_empty($value);
}

/**
  * Connector between checkbox values and key-value storage:
  * Set KV-item from checkbox
  **/
function xcms_set_key_from_checkbox(&$list, $key, $value)
{
    $list[$key] = xcms_checkbox_enabled($value) ? XU_YES : XU_NO;
}
/**
  * Connector between key-value storage and checkbox values.
  * Set checkbox value from KV-item.
  **/
function xcms_get_key_for_checkbox($list, $key)
{
    $bool_value = xcms_is_enabled_key($list, $key);
    return $bool_value ? XCMS_CHECKBOX_ENABLED : XCMS_CHECKBOX_DISABLED;
}


/**
  * Render generic text control
  * Valid types:
  *     input :   generic input field
  *     password: password field
  *     text:     textarea field (TODO: not supported it)
  *     checkbox:
  **/
function xcmst_control($name, $value, $placeholder, $class, $type = "input", $title = "", $def_value = "")
{
    if ($value === XCMS_FROM_POST)
        $value = xcms_get_key_or($_POST, $name, $def_value);
    elseif ($value === XCMS_FROM_GET)
        $value = xcms_get_key_or($_GET, $name, $def_value);

    $value = htmlspecialchars($value);
    $placeholder = htmlspecialchars($placeholder);
    $title = htmlspecialchars($title);

    $type_attr = $type;
    if ($type == "input")
        $type_attr = "text";

    $attrs = "";
    if (xu_not_empty($placeholder))
        $attrs .= " placeholder=\"$placeholder\" ";
    if (xu_not_empty($title))
        $attrs .= " title=\"$title\" ";

    if ($type == "input" || $type == "password")
    {
        echo "<input type=\"$type_attr\" name=\"$name\" id=\"$name-input\" ".
            "value=\"$value\" class=\"$class\" $attrs />";
    }
    elseif ($type == "checkbox")
    {
        if (xcms_checkbox_enabled($value))
            $attrs .= " checked=\"checked\" ";
        $value = $name;
        // prepend fake input with empty value to submit it as checkbox 'unchecked' value
        // See http://iamcam.wordpress.com/2008/01/15/unchecked-checkbox-values/
        echo "<input type=\"hidden\" name=\"$name\" value=\"\"/>".
            "<input type=\"$type_attr\" name=\"$name\" id=\"$name-$type\" ".
            "value=\"$value\" class=\"$class checkbox\" $attrs />";
    }
    else
    {
        echo "Not supported yet. ";
    }
}

/**
  * Specialization for admin-tools
  **/
function xcmst_control_admin($name, $value, $placeholder, $type = "input", $title = "", $def_value = "")
{
    xcmst_control($name, $value, $placeholder, "admin-medium", $type, $title, $def_value);
}
