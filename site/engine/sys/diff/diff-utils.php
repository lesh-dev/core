<?php
    require_once 'finediff.php';

    define('CONTEXT_SIZE', 2);

    /**
      * Diff postprocessing: markup with styles
      **/
    function xcms_diff_postprocess($diff)
    {
        $output = str_replace(EXP_LF, '<br/>'.EXP_LF, $diff);
        $output = str_replace('<skip/>', '<span style="color: #7f7f7f;">***</span>', $output);
        $output = str_replace('<ins>', '<ins style="color: #009f00; text-decoration: none;">', $output);
        $output = str_replace('<del>', '<del style="color: #9f0000;">', $output);
        return $output;
    }

    /**
      * Make html-based diff from text
      **/
    function xcms_diff_html($from_text, $to_text, $post_process = true)
    {
        $opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity /* FineDiff::$characterGranularity */);
        $diff_html = FineDiff::renderDiffToHTMLFromOpcodesContext($from_text, $opcodes);
        if ($post_process)
            $diff_html = xcms_diff_postprocess($diff_html);
        return $diff_html;
    }

    // Test with long text
    function xcms_diff_test()
    {
        global $engine_dir;
        $from_text = file_get_contents("$engine_dir/sys/diff/text.html");
        $to_text = file_get_contents("$engine_dir/sys/diff/newtext.html");
        $diff_html = xcms_diff_html($from_text, $to_text);
        echo $diff_html;
    }

    // Unittest
    function xcms_finediff_unit_test()
    {
        xut_begin("finediff");

        $diff = xcms_diff_html("", "", false);
        xut_equal($diff, "", "Empty equal text");

        $diff = xcms_diff_html("abc", "", false);
        xut_equal($diff, "<del>abc</del> ", "Simple deletion");

        $diff = xcms_diff_html("", "abc", false);
        xut_equal($diff, "<ins>abc</ins>", "Simple insertion");

        $diff = xcms_diff_html("abc def ghi", "abc ghi", false);
        xut_equal($diff, "abc <del>def </del> ghi", "First pbagnall@ patch");

        $diff = xcms_diff_html("\n", "тарам-парам\nпарам-парам\n", false);
        xut_equal($diff, "<del>\n</del> <ins>тарам-парам\nпарам-парам\n</ins>", "Diff lockup");
        // I wish it should be, but it does not want to look forward so much
        //should_be_equal($diff, "<ins>тарам-парам\nпарам-парам</ins>\n", "Diff lockup test");

        $diff = xcms_diff_html("", "тарам-парам\nпарам-парам\n", false);
        xut_equal($diff, "<ins>тарам-парам\nпарам-парам\n</ins>", "Another multiline insertion");

        $diff = xcms_diff_html("тарам-парам", "тарам-парам zyxel\nпарам-парам\n", false);
        xut_equal($diff, "тарам-парам<ins> zyxel\nпарам-парам\n</ins>", "Half-line multiline insertion");

        // Following test covers the difference between original FineDiff behavior
        // that assumes dot is a sentence end. We don't need such precision in levels
        $diff = xcms_diff_html("http://vk.com?bla=value", "https://vk.com?bla=value", false);
        xut_equal($diff, "<del>http://vk.com?bla=value</del> <ins>https://vk.com?bla=value</ins>", "URL diff");

        $diff = xcms_diff_html("abcdefgh aaa", "xyz abcdefgh aaa\ntuv", false);
        xut_equal($diff, "<ins>xyz </ins>abcdefgh aaa<ins>\ntuv</ins>", "Multiline insertion");

        $diff = xcms_diff_html("abcdefgh aaa\n", "xyz abcdefgh aaa\ntuv", false);
        xut_equal($diff, "<ins>xyz </ins>abcdefgh aaa\n<ins>tuv</ins>", "Multiline insertion with newline");

        // Test diffs with html chunks
        $diff = xcms_diff_html("<span>Проверка того</span>", "<span>Замена того</span>", false);
        xut_equal($diff, "&lt;span&gt;<del>Проверка</del> <ins>Замена</ins> того&lt;/span&gt;", "HTML word dividers 1");

        $diff = xcms_diff_html("составляет 10<sup>15</sup> калорий", "составляет 9.5<sup>15</sup> калорий", false);
        xut_equal($diff, "составляет <del>10</del> <ins>9.5</ins>&lt;sup&gt;15&lt;/sup&gt; калорий", "HTML word dividers 2");

        $diff = xcms_diff_html(
            "<p>paragraph One</p>\n".
            "<p>to be inserted before this text Three</p>\n".
            "<p>this is the end of text Four</p>",

            "<p>paragraph One</p>\n".
            "<p>inserted line number Two</p>\n".
            "<p>to be inserted before this text Three</p>\n".
            "<p>this is the end of text Four</p>",

            false);
        xut_equal(
            $diff,
            "&lt;p&gt;paragraph One<ins>&lt;/p&gt;\n".
            "&lt;p&gt;inserted line number Two</ins>&lt;/p&gt;\n".
            "&lt;p&gt;to be inserted before this text Three&lt;/p&gt;\n".
            "&lt;p&gt;this is the end of text Four&lt;/p&gt;",

            "HTML insert line with similar endings");

        xut_end();
    }

?>
