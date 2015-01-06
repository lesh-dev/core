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
  * Canonical way to obtain FIO with nick
  **/
function xsm_fion($person)
{
    $result = xsm_fio($person);
    $nick_name = xcms_get_key_or($person, 'nick_name');
    if (xu_not_empty($nick_name))
        $result .= " ($nick_name)";
    return $result;
}
/**
  * HTML-encoded version of @c xsm_fion
  **/
function xsm_fion_enc($person)
{
    return htmlspecialchars(xsm_fion($person));
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

/**
  * Produce part of SQL WHERE expression for person filter
  **/
function xsm_person_name_filter($db, $show_name_filter)
{
    $show_name_filter = trim($show_name_filter);
    if (!strlen($show_name_filter))
        return '';

    $words = explode(EXP_SP, $show_name_filter);
    $cond = '';
    foreach ($words as $word)
    {
        $w = trim($word);
        if (!strlen($w))
            continue;

        if (strlen($cond))
            $cond .= " AND ";
        $esc_word = $db->escapeString($w);
        $cond .=
            "(".
                "(last_name LIKE '%$esc_word%') OR ".
                "(first_name LIKE '%$esc_word%') OR ".
                "(patronymic LIKE '%$esc_word%') OR ".
                "(nick_name LIKE '%$esc_word%')".
            ")";
    }
    if (!strlen($cond))
        return '';
    return "($cond)";
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