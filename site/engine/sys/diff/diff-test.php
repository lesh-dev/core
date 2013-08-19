<?php
    require_once 'finediff.php';

    function callbackFunc($code, $from, $from_offset, $n)
    {
        print_r("callbackFunc called\n");
        print_r("$code\n");
        print_r("from: $from\n");
        print_r("from_ofs: $from_offset\n");
        print_r("count: $n\n");
        print_r("------------------------\n");

    }

    $from_text = file_get_contents("text.html");
    $to_text = file_get_contents("newtext.html");

    //$from_text = mb_convert_encoding($from_text, 'HTML-ENTITIES', 'UTF-8');
    //$to_text = mb_convert_encoding($to_text, 'HTML-ENTITIES', 'UTF-8');

    //$opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity);
    $opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity);

    //print_r("codes|||$opcodes|||\n");
    $diff_html = FineDiff::renderDiffToHTMLFromOpcodes($from_text, $opcodes);
    echo "<style>
        ins {
            color: #009f00;
            text-decoration: none;
        }
        del {
            color: #9f0000;
        }
    </style>";
    echo $diff_html;
?>
