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
        global $xut_current_fail_count;
        global $xut_current_check_success_count;
        $xut_current_fail_count = 0;
        $xut_current_check_success_count = 0;
        echo "<div style=\"font-weight: bold;\">Running test <tt style=\"color: #00007f\">$test_name</tt></div>";
        echo "<pre style=\"margin: 0px\">\n";
    }

    function xut_end()
    {
        global $xut_current_fail_count;
        global $xut_current_check_success_count;
        echo "    $xut_current_check_success_count passed, $xut_current_fail_count failed\n";
        echo "</pre>\n";
    }

    function _xut_fail()
    {
        global $xut_fail_count;
        global $xut_current_fail_count;
        $xut_fail_count++;
        $xut_current_fail_count++;
    }

    function _xut_success()
    {
        global $xut_check_success_count;
        global $xut_current_check_success_count;
        $xut_check_success_count++;
        $xut_current_check_success_count++;
    }

    function xut_report($message)
    {
        _xut_fail();
        echo "$message\n";
    }

    function xut_check($condition, $message)
    {
        if ($condition)
        {
            _xut_success();
            return;
        }
        xut_report($message);
    }

    function xut_equal($left, $right, $message)
    {
        if ($left === $right)
        {
            _xut_success();
            return;
        }

        xut_report("$message:<br>'<span style=\"color: #007f00;\">".
            htmlspecialchars($left)."</span>'<br>===<br>'<span style=\"color: #7f0000;\">".
            htmlspecialchars($right)."</span>'</br>failed");
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
