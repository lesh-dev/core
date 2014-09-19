<?php
/**
  * Canonical way to obtain FIO
  **/
function xsm_fio($person)
{
    return
        xcms_get_key_or($person, 'last_name').' '.
        xcms_get_key_or($person, 'first_name').' '.
        xcms_get_key_or($person, 'patronymic');
}
/**
  * HTML-encoded version of @c xsm_fio
  **/
function xsm_fio_enc($person)
{
    return htmlspecialchars(xsm_fio($person));
}

/**
  * Canonical way to obtain FI
  **/
function xsm_fi($person, $prefix = '')
{
    return $person["${prefix}last_name"].' '.$person["${prefix}first_name"];
}
/**
  * HTML-encoded version of @c xsm_fi
  **/
function xsm_fi_enc($person, $prefix = '')
{
    return htmlspecialchars(xsm_fi($person, $prefix));
}

function xsm_get_roles($obj)
{
    // TODO: curatorship
    $roles = array();
    if (xcms_checkbox_enabled($obj["is_teacher"]))
        $roles[] = "Препод";
    if (xcms_checkbox_enabled($obj["is_student"]))
        $roles[] = "Школьник";
    return implode(", ", $roles);
}

?>