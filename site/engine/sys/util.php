<?php

include_once("$engine_dir/sys/tag.php");
include_once("$engine_dir/sys/file.php");

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

?>