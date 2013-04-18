<?php

include_once("$engine_dir/sys/tag.php");

function xcms_hostname()
{
    $host = @shell_exec("hostname -f");
    if (empty($host))
        $host = xcms_get_key_or($_SERVER, "HTTP_HOST");
    return $host;
}

?>