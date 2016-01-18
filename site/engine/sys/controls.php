<?php

require_once("${engine_dir}sys/string.php");
require_once("${engine_dir}sys/tag.php");

define('XCMS_FROM_POST', '{{{XCMS_FROM_POST}}}');
define('XCMS_FROM_GET', '{{{XCMS_FROM_GET}}}');
define('XCMS_CHECKBOX_ENABLED', 'enabled');
define('XCMS_CHECKBOX_DISABLED', '');

define('XCMS_AUTOCOMPLETE_DEFAULT', 'default');
define('XCMS_AUTOCOMPLETE', 'on');
define('XCMS_NO_AUTOCOMPLETE', 'off');

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
  *     text:     textarea field (TODO: not supported yet)
  *     checkbox:
  **/
function xcmst_control($name, $value, $placeholder, $class, $type = "input", $title = "", $def_value = "", $autocomplete = XCMS_AUTOCOMPLETE_DEFAULT)
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
        $au = "";
        if ($autocomplete != XCMS_AUTOCOMPLETE_DEFAULT)
            $au = " autocomplete=\"$autocomplete\" ";
        echo "<input type=\"$type_attr\" name=\"$name\" id=\"$name-input\" $au ".
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
function xcmst_control_admin($name, $value, $placeholder, $type = "input", $title = "", $def_value = "", $autocomplete = XCMS_AUTOCOMPLETE_DEFAULT)
{
    xcmst_control($name, $value, $placeholder, "admin-medium", $type, $title, $def_value, $autocomplete);
}

/**
  * Proper selected attribute formatting
  **/
function xcms_enum_selected($value, $current_value)
{
    return ((string)($value) == (string)($current_value)) ? ' selected="selected" ' : '';
}

function xcms_sys_controls_unit_test()
{
    xut_begin("sys-controls");

    xut_check(xcms_enum_selected("", "0") === "", "Enum selection false positive");
    xut_check(strpos(xcms_enum_selected("", ""), "selected") !== false, "Enum selection true");
    xut_check(strpos(xcms_enum_selected("1", 1), "selected") !== false, "Enum selection digits");

    xut_end();
}

