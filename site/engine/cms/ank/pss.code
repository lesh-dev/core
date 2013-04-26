<?php
// Persistent session keys storage
function xcms_get_persistent_key($key_prefix, $key_name, $default_value = '')
{
    $value = $default_value;
    $session_key = "$key_prefix::$key_name";
    if (array_key_exists($key_name, $_POST))
    {
        $value = $_POST[$key_name];
        $_SESSION[$session_key] = $value; // update value in cache
    }
    elseif (array_key_exists($key_name, $_GET))
    {
        $value = $_GET[$key_name];
        $_SESSION[$session_key] = $value; // update value in cache
    }
    elseif (array_key_exists($session_key, $_SESSION))
    {
        $value = $_SESSION[$session_key];
    }
    return $value;
}
?>