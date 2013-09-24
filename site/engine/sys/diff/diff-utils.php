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
        xut_check($diff === "", "Empty equal text");

        $diff = xcms_diff_html("abc", "", false);
        xut_check($diff === "<del>abc</del>", "Simple deletion");

        $diff = xcms_diff_html("", "abc", false);
        xut_check($diff === "<ins>abc</ins>", "Simple insertion");

        $diff = xcms_diff_html("abcdefgh aaa", "xyz abcdefgh aaa\ntuv", false);
        xut_check($diff === "<ins>xyz </ins>abcdefgh <del>aaa</del><ins>aaa\ntuv</ins>", "Multiline insertion");

        $diff = xcms_diff_html("abcdefgh aaa\n", "xyz abcdefgh aaa\ntuv", false);
        xut_check($diff === "<ins>xyz </ins>abcdefgh aaa\n<ins>tuv</ins>", "Multiline insertion with newline");

        //echo "|".htmlspecialchars($diff)."|";
        xut_end();
    }

?>
