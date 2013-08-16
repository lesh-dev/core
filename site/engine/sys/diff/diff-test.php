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

    $from_text = "проверка utf8";
    $to_text = "проверка   не Utf8";

    //$from_text = mb_convert_encoding($from_text, 'HTML-ENTITIES', 'UTF-8');
    //$to_text = mb_convert_encoding($to_text, 'HTML-ENTITIES', 'UTF-8');

    //$opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity);
    $opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$characterGranularity);

    print_r("codes|||$opcodes|||\n");
    $diff_html = FineDiff::renderDiffToHTMLFromOpcodes($from_text, $opcodes);
    echo $diff_html;

    //$from_text = mb_convert_encoding($from_text_utf8, 'HTML-ENTITIES', 'UTF-8');
    //$to_text = mb_convert_encoding($to_text_utf8, 'HTML-ENTITIES', 'UTF-8');
    //print(mb_convert_encoding($diffHTML, 'UTF-8', 'HTML-ENTITIES'));


    //FineDiff::renderFromOpcodes($from_text, $opcodes, "callbackFunc");

    //print_r(mb_convert_encoding($opcodes, 'UTF-8', 'HTML-ENTITIES')."\n");

?>
