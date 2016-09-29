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

define('XCMS_AUTOCAPITALIZE_DEFAULT', 'default');
define('XCMS_AUTOCAPITALIZE', 'on');
define('XCMS_NO_AUTOCAPITALIZE', 'off');


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
  * Assigns fresh and uniique control id
  **/
function xcms_add_control_id($id_template)
{
    global $XCMS_CONTROL_IDS;
    if (!is_array($XCMS_CONTROL_IDS))
        $XCMS_CONTROL_IDS = array();

    for ($i = 0; $i < 256; ++$i)
    {
        $suffix = "";
        if ($i > 0)
            $suffix = "$i";
        $id = $id_template.$suffix;
        if (!array_key_exists($id, $XCMS_CONTROL_IDS))
        {
            $XCMS_CONTROL_IDS[$id] = true;
            return $id;
        }
    }
    xcms_log(XLOG_ERROR, "xcms_add_control_id error");
    die("ERROR: xcms_add_control_id failed, please report to dev@fizlesh.ru");
}

/**
  * Render generic text control
  * Valid types:
  *     input :   generic input field
  *     password: password field
  *     text:     textarea field (TODO: not supported yet)
  *     checkbox: checkbox control
  *     submit:   submit (button) control
  **/
function xcmst_control($name, $value, $placeholder, $class, $type = "input", $title = "", $def_value = "", $autocomplete = XCMS_AUTOCOMPLETE_DEFAULT, $autocapitalize = XCMS_AUTOCAPITALIZE_DEFAULT)
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
        $complete = "";
        if ($autocomplete != XCMS_AUTOCOMPLETE_DEFAULT)
            $complete = " autocomplete=\"$autocomplete\" ";

        $capitalize = "";
        if ($autocapitalize != XCMS_AUTOCAPITALIZE_DEFAULT)
            $capitalize = " autocapitalize=\"$autocapitalize\" ";

        $id = xcms_add_control_id("$name-input");
        echo "<input type=\"$type_attr\" name=\"$name\" id=\"$id\" $complete $capitalize ".
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
    elseif ($type == "submit")
    {
        $id = xcms_add_control_id("$name-submit");
        echo "<input type=\"submit\" name=\"$name\" id=\"$id\" value=\"$value\" class=\"$class\" $attrs/>";
    }
    elseif ($type == "hidden")
    {
        echo "<input type=\"hidden\" name=\"$name\" value=\"$value\" $attrs/>";
    }
    else
    {
        echo "<b style=\"color: red;\">ERROR:</b> Controls of type '$type' [name: $name] are not supported yet.\n";
    }
}

function xcmst_submit($name, $value, $title = "", $class = "")
{
    xcmst_control($name, $value, "", $class, "submit", $title);
}

function xcmst_hidden($name, $value)
{
    xcmst_control($name, $value, "", "", "hidden");
}

function xcmst_link($url, $id, $inner_html, $title = "", $class = "")
{
    $title = htmlspecialchars($title);
    echo "<a class=\"$class\" id=\"$id\" href=\"$url\" title=\"$title\">$inner_html</a>";
}

/**
  * Specialization for admin-tools
  * Disable auto-capitalization: #919
  **/
function xcmst_control_admin($name, $value, $placeholder, $type = "input", $title = "", $def_value = "", $autocomplete = XCMS_AUTOCOMPLETE_DEFAULT, $autocapitalize = XCMS_NO_AUTOCAPITALIZE)
{
    xcmst_control($name, $value, $placeholder, "admin-medium", $type, $title, $def_value, $autocomplete, $autocapitalize);
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

