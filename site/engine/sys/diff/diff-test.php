<?php
    include './finediff-code.php';


    function callbackFunc($code, $from, $from_offset, $n)
    {
        print_r("callbackFunc called\n");
        print_r("$code\n");
        print_r("from: $from\n");
        print_r("from_ofs: $from_offset\n");
        print_r("count: $n\n");
        print_r("------------------------\n");

    }

    $from_text_utf8 = "Проверка&amp; utf8";
    $to_text_utf8 = "Проверка не Utf8";

    $from_text = mb_convert_encoding($from_text_utf8, 'HTML-ENTITIES', 'UTF-8');
    $to_text = mb_convert_encoding($to_text_utf8, 'HTML-ENTITIES', 'UTF-8');

    $opcodes = FineDiff::getDiffOpcodes($from_text, $to_text, FineDiff::$wordGranularity);


    //print_r("codes|||$opcodes|||\n");
    $diffHTML = FineDiff::renderDiffToHTMLFromOpcodes($from_text, $opcodes);

    //$from_text = mb_convert_encoding($from_text_utf8, 'HTML-ENTITIES', 'UTF-8');
    //$to_text = mb_convert_encoding($to_text_utf8, 'HTML-ENTITIES', 'UTF-8');
    print(mb_convert_encoding($diffHTML, 'UTF-8', 'HTML-ENTITIES'));


    //FineDiff::renderFromOpcodes($from_text, $opcodes, "callbackFunc");

    //print_r(mb_convert_encoding($opcodes, 'UTF-8', 'HTML-ENTITIES')."\n");

?>
