<?php

include_once("$engine_dir/sys/tag.php");
include_once("$engine_dir/sys/file.php");

function xcms_hostname()
{
    global $meta_site_url;
    if ($meta_site_url)
        $host = preg_replace('#http(s|)://(.*?)(/|$)#', '\2', $meta_site_url);

    if (empty($host))
        $host = xcms_get_key_or($_SERVER, "HTTP_HOST");

    if (empty($host))
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
    if (empty($pass))
    {
        $table = array();
        for ($i = 0; $i < 26; $i++)
            $table[] = chr($i + 65);
        $table[] = '@';
        $table[] = '-';
        $table[] = '_';
        $size = count($table);
        for ($i = 0; $i < 12; $i++)
            $pass .= $table[rand($i * $i) % $size];
    }
    return $pass;
}

/**
  * YYYY-MM-DD HH:MM:SS
  **/
function xcms_datetime($timestamp = false)
{
    if ($timestamp === false)
        return date("Y-m-d H:i:s");
    if (empty($timestamp))
        return "";
    return date("Y-m-d H:i:s", $timestamp);
}

function xcms_date($timestamp = false)
{
    if ($timestamp === false)
        return date("Y-m-d");
    if (empty($timestamp))
        return "";
    return date("Y-m-d", $timestamp);
}

function xcms_rus_date($timestamp = false)
{
    if ($timestamp === false)
        return date("d.m.Y");
    if (empty($timestamp))
        return "";
    return date("d.m.Y", $timestamp);
}

// Reverse to xcms_datetime
function xcms_datetime_to_ts($date_time)
{
    return strtotime($date_time);
}

function xcms_get_html_template($template_name)
{
    global $SETTINGS;
    $full_name = "{$SETTINGS['engine_dir']}templates/$template_name.html";
    if (!file_exists($full_name))
    {
        xcms_log(XLOG_ERROR, "Template '$full_name' not found");
        return "";
    }
    return @file_get_contents($full_name);
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