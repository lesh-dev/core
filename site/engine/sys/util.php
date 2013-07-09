<?php

include_once("$engine_dir/sys/tag.php");

function xcms_hostname()
{
    $host = xcms_get_key_or($_SERVER, "HTTP_HOST");
    if (empty($host))
    {
        $host = @shell_exec("hostname -f");
        $host = trim($host);
    }
    return $host;
}

function xcms_write($file_name, $contents)
{
    $f = fopen($file_name, "wb");
    if (!$f)
        return false;
    fwrite($f, $contents);
    fclose($f);
    return true;
}

function xcms_append($file_name, $contents)
{
    $f = fopen($file_name, "a+b");
    if (!$f)
        return false;
    fwrite($f, $contents);
    fclose($f);
    return true;
}

?>