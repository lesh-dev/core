<?php

require_once("${xengine_dir}sys/logger.php");
require_once("${xengine_dir}sys/auth.php");

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
