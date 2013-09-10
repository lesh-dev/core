<?php
    require_once 'finediff.php';

    define('CONTEXT_SIZE', 2);

    /**
      * Diff postprocessing: markup with styles
      **/
    function xcms_diff_postprocess($diff)
    {
        $output = "";

        $ad = explode(EXP_LF, $diff);
        $show = array();
        for ($i = 0; $i < count($ad); ++$i)
            $show[$i] = false;

        for ($i = 0; $i < count($ad); ++$i)
        {
            $ln = $ad[$i];
            if (strpos($ln, "<ins>") !== false ||
                strpos($ln, "<del>") !== false)
            {
                for ($j = $i - CONTEXT_SIZE; $j <= $i + CONTEXT_SIZE; ++$j)
                    if ($j >= 0 && $j < count($show))
                        $show[$j] = true;

            }
        }
        $dots = false;
        for ($i = 0; $i < count($show); ++$i)
        {
            $ln = $ad[$i];
            if ($show[$i])
            {
                $ln = str_replace("\n", "", $ln);
                $ln = str_replace("\r", "", $ln);
                $output .= "<div>$ln</div>\n";
                $dots = false;
            }
            else
            {
                if ($dots)
                    continue;
                $dots = true;
                $output .= '<div style="color: #7f7f7f;">***</div>'."\n";
            }
        }
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
        $diff_html = FineDiff::renderDiffToHTMLFromOpcodes($from_text, $opcodes);
        $diff_html = xcms_diff_postprocess($diff_html);
        return $diff_html;
    }

    // Test
    function xcms_diff_test()
    {
        $from_text = file_get_contents("text.html");
        $to_text = file_get_contents("newtext.html");
        $diff_html = xcms_diff_html($from_text, $to_text);
        echo $diff_html;
    }
?>
