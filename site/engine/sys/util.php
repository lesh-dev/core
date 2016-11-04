<?php

require_once("${engine_dir}sys/string.php");
require_once("${engine_dir}sys/file.php");

/**
  * Transforms an key-value-array to properly encoded URI part:
  * array("param" => "value1 value2", "super" => "puper") will be translated to
  * "&amp;param=value1%20value2&amp;super=puper"
  * @param args_list array of arguments to encode
  * @return encoded parameters string
  **/
function xcms_url($args_list)
{
    $res = '';
    foreach ($args_list as $key => $value)
    {
        $res = "$res&amp;$key=".rawurlencode($value);
    }
    return $res;
}

/**
  * Same as @sa xcms_url, but makes complete href="..." attribute
  * containing given parameters
  * @param args_list array of arguments to encode
  * @return encoded parameters string
  **/
function xcms_href($args_list)
{
    return ' href="?'.xcms_url($args_list).'" ';
}

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

/**
  * External link to XSM view
  * @param url_prefix (interpreted as aparam after rewrite)
  * @param args_list array of arguments to encode
  * @return complete link with scheme and server name to use as link
  * on (external to site) pages, e.g. in-mail links, etc
  **/
function xsm_ext_href($url_prefix, $args_list)
{
    global $web_prefix;
    $url = 'https://'.xcms_hostname().
        "/${web_prefix}xsm/$url_prefix".xcms_url($args_list);
    return " href=\"$url\" ";
}

/**
  * Filters generated password from bad chars
  **/
function _xcms_filter_passwd($passwd)
{
    $passwd = preg_replace("/[^A-Za-z0-9]/", "", $passwd);
    $passwd = preg_replace("/[OoIi1]/", "", $passwd);
    return substr($passwd, 0, 12);
}

/**
  * Generates new password
  **/
function xcms_mkpasswd()
{
    $pass = trim(@shell_exec("mkpasswd")).trim(@shell_exec("mkpasswd")).trim(@shell_exec("mkpasswd"));
    $pass = _xcms_filter_passwd($pass);
    if (xu_empty($pass))
    {
        $table = array();
        for ($i = 0; $i < 26; $i++)
        {
            $table[] = chr($i + 65);
        }
        for ($i = 0; $i < 10; $i++)
            $table[] = chr($i + 48);
        $size = count($table);
        for ($i = 0; $i < 32; $i++)
        {
            $max = ($i + 256) * ($i + 20);
            $pass .= $table[mt_rand(0, $max) % $size];
        }
        $pass = _xcms_filter_passwd($pass);
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
  * Human-readable timestamp
  **/
function xcms_datetime($timestamp = false)
{
    if ($timestamp === false)
        return date("Y-m-d H:i:s");
    if (xu_empty($timestamp))
        return "";
    return date("Y-m-d H:i:s", $timestamp);
}

/**
  * YYYY-MM-DD.HH-MM-SS
  * Human-readable timestamp without spaces, suitable for filenames
  **/
function xcms_datetime_ns($timestamp = false)
{
    if ($timestamp === false)
        return date("Y-m-d.H-i-s");
    if (xu_empty($timestamp))
        return "";
    return date("Y-m-d.H-i-s", $timestamp);
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

function xcms_util_unit_test()
{
    xut_begin("util");

    global $meta_site_url;
    $meta_site_url = "https://rc.fizlesh.ru/";
    xut_equal(xcms_hostname(), "rc.fizlesh.ru", "xcms_hostname does not work");

    $meta_site_url = "http://test.fizlesh.ru";
    xut_equal(xcms_hostname(), "test.fizlesh.ru", "xcms_hostname does not work");

    for ($i = 0; $i < 100; ++$i)
    {
        $passwd = xcms_mkpasswd();
        xut_equal(xu_len($passwd), 12, "Password '$passwd' is not 12-char");
        xut_check(
            strstr($passwd, 'O') === false &&
            strstr($passwd, 'o') === false &&
            strstr($passwd, '1') === false &&
            strstr($passwd, 'I') === false &&
            strstr($passwd, 'i') === false,
            "Password '$passwd' contains bad chars."
        );
    }

    xut_end();
}

?>