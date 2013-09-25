<?php

    global $xut_fail_count;
    global $xut_check_success_count;

    function xut_initialize()
    {
        global $xut_fail_count;
        global $xut_check_success_count;
        $xut_fail_count = 0;
        $xut_check_success_count = 0;
    }

    function xut_begin($test_name)
    {
        echo "<div style=\"font-weight: bold;\">Running test <tt style=\"color: #00007f\">$test_name</tt></div>";
        echo "<pre style=\"margin: 0px\">\n";
    }


    function xut_end()
    {
        echo "</pre>\n";
    }

    function xut_report($message)
    {
        global $xut_fail_count;
        $xut_fail_count++;
        echo "$message\n";
    }

    function xut_check($condition, $message)
    {
        global $xut_check_success_count;
        if ($condition)
        {
            $xut_check_success_count++;
            return;
        }
        xut_report($message);
    }

    function xut_equal($left, $right, $message)
    {
        global $xut_check_success_count;
        if ($left === $right)
        {
            $xut_check_success_count++;
            return;
        }

        xut_report("$message: '<span style=\"color: #007f00;\">".
            htmlspecialchars($left)."</span>' === '<span style=\"color: #7f0000;\">".
            htmlspecialchars($right)."</span>' failed");
    }

    function xut_finalize()
    {
        global $xut_fail_count;
        global $xut_check_success_count;

        echo "<div><span style=\"color: #007f00;\">Success checks:</span> <b>$xut_check_success_count</b></div>\n";
        echo "<div><span style=\"color: #7f0000;\">Failed checks:</span> <b>$xut_fail_count</b></div>\n";
        if ($xut_fail_count == 0)
            echo "<div style=\"color: #007f00; font-size: 14pt; font-weight: bold;\"><span >UNIT TESTS PASSED OK</div>\n";
        else
            echo "<div style=\"color: #7f0000; font-size: 14pt; font-weight: bold;\"><span >UNIT TESTS FAILED<div>\n";
    }
?>