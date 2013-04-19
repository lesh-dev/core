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

?>