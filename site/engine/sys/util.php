<?php

require_once("${engine_dir}sys/string.php");
require_once("${engine_dir}sys/tag.php");
require_once("${engine_dir}sys/file.php");

function xcms_hostname()
{
    global $meta_site_url;
    if ($meta_site_url)
        $host = preg_replace('#http(s|)://(.*?)(/|$)#', '\2', $meta_site_url);

    if (xu_empty($host))
        $host = xcms_get_key_or($_SERVER, "HTTP_HOST");

    if (xu_empty($host))
    {
        $host = @shell_exec("hostname -f");
        $host = trim($host);
    }

    return $host;
}

function xcms_mkpasswd()
{
    $pass = trim(@shell_exec("mkpasswd")).trim(@shell_exec("mkpasswd"));
    $pass = preg_replace("/[^A-Za-z0-9_-]/", "@", $pass);
    $pass = substr($pass, 0, 12);
    if (xu_empty($pass))
    {
        $table = array();
        for ($i = 0; $i < 26; $i++)
            $table[] = chr($i + 65);
        $table[] = '@';
        $table[] = '-';
        $table[] = '_';
        $size = count($table);
        for ($i = 0; $i < 12; $i++)
            $pass .= $table[mt_rand(0, $i * $i) % $size];
    }
    return $pass;
}

/**
  * Generate v4 UUID (do not mix with GUID)
  * Copy-pasted from http://stackoverflow.com/questions/2040240/php-function-to-generate-v4-uuid
  **/
function xcms_uuid()
{
    return sprintf( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
        // 32 bits for "time_low"
        mt_rand(0, 0xffff), mt_rand(0, 0xffff),

        // 16 bits for "time_mid"
        mt_rand(0, 0xffff),

        // 16 bits for "time_hi_and_version",
        // four most significant bits holds version number 4
        mt_rand(0, 0x0fff) | 0x4000,

        // 16 bits, 8 bits for "clk_seq_hi_res",
        // 8 bits for "clk_seq_low",
        // two most significant bits holds zero and one for variant DCE1.1
        mt_rand(0, 0x3fff) | 0x8000,

        // 48 bits for "node"
        mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
    );
}

/**
  * YYYY-MM-DD HH:MM:SS
  **/
function xcms_datetime($timestamp = false)
{
    if ($timestamp === false)
        return date("Y-m-d H:i:s");
    if (xu_empty($timestamp))
        return "";
    return date("Y-m-d H:i:s", $timestamp);
}

function xcms_date($timestamp = false)
{
    if ($timestamp === false)
        return date("Y-m-d");
    if (xu_empty($timestamp))
        return "";
    return date("Y-m-d", $timestamp);
}

function xcms_rus_date($timestamp = false)
{
    if ($timestamp === false)
        return date("d.m.Y");
    if (xu_empty($timestamp))
        return "";
    return date("d.m.Y", $timestamp);
}

// Reverse to xcms_datetime
function xcms_datetime_to_ts($date_time)
{
    return strtotime($date_time);
}

/**
  * Get template contents by name
  **/
function xcms_get_html_template($template_name)
{
    global $SETTINGS;
    $full_name = "{$SETTINGS['engine_dir']}templates/$template_name.html";
    if (!file_exists($full_name))
    {
        xcms_log(XLOG_ERROR, "[KERNEL] Template '$full_name' not found");
        return "";
    }
    return @file_get_contents($full_name);
}

/**
  * Get template and replace common things there
  **/
function xcms_prepare_html_template($template_name)
{
    $body_html = xcms_get_html_template($template_name);
    $login = xcms_user()->login();
    $real_name = xcms_user()->param("name");
    $body_html = str_replace('@@LOGIN@', $login, $body_html);
    $body_html = str_replace('@@REAL-NAME@', $real_name, $body_html);
    return $body_html;
}

function xcms_util_unit_test()
{
    xut_begin("util");

    global $meta_site_url;
    $meta_site_url = "https://rc.fizlesh.ru/";
    xut_equal(xcms_hostname(), "rc.fizlesh.ru", "xcms_hostname does not work");

    $meta_site_url = "http://test.fizlesh.ru";
    xut_equal(xcms_hostname(), "test.fizlesh.ru", "xcms_hostname does not work");

    xut_end();
}

?>