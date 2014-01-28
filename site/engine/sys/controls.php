<?php

require_once("${engine_dir}sys/string.php");

define('XCMS_FROM_POST', '{{{XCMS_FROM_POST}}}');
define('XCMS_FROM_GET', '{{{XCMS_FROM_GET}}}');

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

/**
  * Generic checkbox generator. Has derivatives in XSM
  * TODO: translate to template
  **/
function xcms_make_checkbox($name, $value, $checked_value, $class)
{
    if (xu_not_empty($value))
        $checked = 'checked="checked"';
    else
        $checked = '';
    // prepend fake input with empty value to submit it as checkbox 'unchecked' value
    // See http://iamcam.wordpress.com/2008/01/15/unchecked-checkbox-values/
    $html =
        "<input type=\"hidden\" name=\"$name\" value=\"\"/>".
        "<input class=\"$class checkbox\" type=\"checkbox\" name=\"$name\" ".
            "id=\"$name-checkbox\" value=\"$checked_value\" $checked />";
    return $html;
}

/**
  * Render generic text control
  * TODO: Add textarea support here
  **/
function xcmst_control($name, $value, $placeholder, $class, $type = "text")
{
    if ($value === XCMS_FROM_POST)
        $value = xcms_get_key_or($_POST, $name);
    elseif ($value === XCMS_FROM_GET)
        $value = xcms_get_key_or($_GET, $name);

    $value = htmlspecialchars($value);
    $placeholder = htmlspecialchars($placeholder);

    $attrs = "";
    if (xu_not_empty($placeholder))
        $attrs .= " placeholder=\"$placeholder\" ";

    echo "<input type=\"$type\" name=\"$name\" id=\"$name-input\" ".
        "value=\"$value\" class=\"$class\" $attrs />";
}

/**
  * Specialization for admin-tools
  **/
function xcmst_control_admin($name, $value, $placeholder, $type = "text")
{
    xcmst_control($name, $value, $placeholder, "admin-medium", $type);
}

/** Generic text input attributes generator
  * including value taken from POST request
  **/
function xcmst_input_attrs_from_post($key, $placeholder = "")
{
    $attrs = "class=\"admin-medium\" id=\"$key-input\" name=\"$key\" value=\"".
        htmlspecialchars(xcms_get_key_or($_POST, $key))."\"";
    if (xu_not_empty($placeholder))
        $attrs .= " placeholder=\"".htmlspecialchars($placeholder)."\" ";
    echo $attrs;
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
