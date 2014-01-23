<?php

define('YES', "yes");
define('NO', "no");

/**
  * Return proper checkbox attributes
  * for KV storage item
  **/
function xcms_checkbox_attr($val)
{
    $attr = ' value="'.YES.'" ';
    if ($val == YES)
        $attr .= ' checked="checked" ';
    return $attr;
}

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
function xcmst_checkbox_attrs_from_post($key, $def_value = NO)
{
    $value = $def_value;
    if (array_key_exists($key, $_POST))
        $value = $_POST[$key];

    echo "id=\"$key-checkbox\" name=\"$key\" ".
        xcms_checkbox_attr($value);
}
