<?php
function _format_pss_id($pss_key)
{
    $user = xcms_user()->login();
    return "$user::$pss_key";
}

function _store_pss_key($pss_key, $value)
{
    $pss_id = _format_pss_id($pss_key);
    $values = array(
        "pss_id" => $pss_id,
        "pss_value" => $value,
    );
    $pss_data = xdb_get_entity_by_id("pss", $pss_id, true);
    if (!$pss_data)
    {
        xdb_insert_ai("pss", array("pss_id"), $values, $values, XDB_OVERRIDE_TS, XDB_NO_USE_AI, $outer_db = $db);
    }
    else
    {
        xdb_update("pss", array("pss_id" => $pss_id), $values, $values);
    }
}

function _get_pss_key($pss_key, $default_value)
{
    $pss_id = _format_pss_id($pss_key);
    $pss_record = xdb_get_entity_by_id("pss", $pss_id, true);
    return xcms_get_key_or($pss_record, "pss_value", $default_value);
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
    else
    {
        $value = _get_pss_key($pss_key, $default_value);
    }
    return $value;
}
