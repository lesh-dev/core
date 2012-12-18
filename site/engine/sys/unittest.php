<?php

    global $xut_fail_count;

    function xut_initialize()
    {
        global $xut_fail_count;
        $xut_fail_count = 0;
        echo "<pre>";
    }

    function xut_report($message)
    {
        global $xut_fail_count;
        $xut_fail_count++;
        echo "$message<br />\n";
    }

    function xut_check($condition, $message)
    {
        if ($condition)
            return;
        xut_report($message);
    }

    function xut_finalize()
    {
        echo "</pre>";
        echo 'Voila!';
    }
?>