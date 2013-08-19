<?php
    require_once 'finediff.php';

    define('CONTEXT_SIZE', 2);

    function diff_postprocess($diff)
    {
        $output = "";

        $ad = explode("\n", $diff);
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
                $output .= "<div>$ln</div>\n";
                $dots = false;
            }
            else
            {
                if ($dots)
                    continue;
                $dots = true;
                $output .= "<div style=\"color: #7f7f7f;\">***</div>\n";
            }
        }
        return $output;
    }

    $from_text = file_get_contents("text.html");
    $to_text = file_get_contents("newtext.html");

    //$opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$characterGranularity);
    $opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity);

    $diff_html = FineDiff::renderDiffToHTMLFromOpcodes($from_text, $opcodes);
    echo "<style>
        body {
            font-family: monospace;
        }
        ins {
            color: #009f00;
            text-decoration: none;
        }
        del {
            color: #9f0000;
        }
    </style>";

    $diff_html = diff_postprocess($diff_html);
    echo $diff_html;
?>
