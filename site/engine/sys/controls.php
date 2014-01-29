<?php

require_once("${engine_dir}sys/string.php");

define('XCMS_FROM_POST', '{{{XCMS_FROM_POST}}}');
define('XCMS_FROM_GET', '{{{XCMS_FROM_GET}}}');
define('XCMS_CHECKBOX_ENABLED', 'enabled');
define('XCMS_CHECKBOX_DISABLED', '');

/**
  * Return proper checkbox attributes
  * for KV storage item
  **/
function xcms_checkbox_attr($val)
{
    $attr = ' value="'.XU_YES.'" ';
    if ($val == XU_YES)
        $attr .= ' checked="checked" ';
    return $attr;
}

function xcms_checkbox_enabled($value)
{
    return xu_not_empty($value);
}

/**
  * Generic checkbox generator. Has derivatives in XSM
  * TODO: translate to template
  **/
function xcms_make_checkbox($name, $value, $checked_value, $class)
{
    if (xcms_checkbox_enabled($value))
        $checked = 'checked="checked"';
    else
        $checked = '';
    $html =
        "<input type=\"hidden\" name=\"$name\" value=\"\"/>".
        "<input class=\"$class checkbox\" type=\"checkbox\" name=\"$name\" ".
            "id=\"$name-checkbox\" value=\"$checked_value\" $checked />";
    return $html;
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

/**
  * Same as previous function, but for checkboxes
  **/
function xcmst_checkbox_attrs_from_post($key, $def_value = XU_NO)
{
    $value = $def_value;
    if (array_key_exists($key, $_POST))
        $value = $_POST[$key];

    echo "id=\"$key-checkbox\" name=\"$key\" ".
        xcms_checkbox_attr($value);
}
