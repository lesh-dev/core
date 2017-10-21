<?php
function _store_pss_key($pss_key, $value)
{
    $user = xcms_user()->login();
    $full_key = "user::$pss_key";
    $values = array(
        "pss_key" => $full_key,
        "pss_value" => $value,
    );
    xdb_insert_or_update("pss", array("pss_key" => $pss_key), $values, $values);
}

function _get_pss_key($pss_key, $value)
{
    $user = xcms_user()->login();
    $full_key = "user::$pss_key";
    $values = array(
        "pss_key" => $full_key,
        "pss_value" => $value,
    );
    $pss_record = xdb_get_entity_by_id("pss", $full_key);
    return xcms_get_key_or($pss_record, "pss_value");
}

// Persistent session keys storage
function xcms_get_persistent_key($key_prefix, $key_name, $default_value = '')
{
    $value = $default_value;

    $pss_key = "$key_prefix::$key_name";
    if (array_key_exists($key_name, $_POST))
    {
        $value = $_POST[$key_name];
        _store_pss_key($pss_key, $value);
    }
    elseif (array_key_exists($key_name, $_GET))
    {
        $value = $_GET[$key_name];
        _store_pss_key($pss_key, $value);
    }
    elseif (array_key_exists($session_key, $_SESSION))
    {
        $value = _get_pss_key($pss_key);
    }
    return $value;
}
