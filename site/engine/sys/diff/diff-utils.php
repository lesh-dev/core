<?php
    require_once 'finediff.php';

    define('CONTEXT_SIZE', 2);

    /**
      * Diff postprocessing: markup with styles
      **/
    function xcms_diff_postprocess($diff)
    {
        $output = str_replace(EXP_LF, '<br/>', $diff);
        $output = str_replace('<skip/>', '<span style="color: #7f7f7f;">***</span>', $output);
        $output = str_replace('<ins>', '<ins style="color: #009f00; text-decoration: none;">', $output);
        $output = str_replace('<del>', '<del style="color: #9f0000;">', $output);
        return $output;
    }

    /**
      * Make html-based diff from text
      **/
    function xcms_diff_html($from_text, $to_text)
    {
        $opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity /* FineDiff::$characterGranularity */);
        $diff_html = FineDiff::renderDiffToHTMLFromOpcodesContext($from_text, $opcodes);
        $diff_html = xcms_diff_postprocess($diff_html);
        return $diff_html;
    }

    // Test
    function xcms_diff_test()
    {
        global $engine_dir;
        $from_text = file_get_contents("$engine_dir/sys/diff/text.html");
        $to_text = file_get_contents("$engine_dir/sys/diff/newtext.html");
        $diff_html = xcms_diff_html($from_text, $to_text);
        echo $diff_html;
    }
?>
