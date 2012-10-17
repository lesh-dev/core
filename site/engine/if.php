<?php
    $input = explode("//", $code);
    foreach ($input as $key=>$value)
    {
        $input[$key] = str_replace("//", "", $value);
    }

    $cond = $input[1];
    $then = $input[2];
    @$else = $input[3];

    @$elem_dir = $SETTINGS["engine_dir"];
    @$then_source = "$elem_dir$then.xcms";
    @$else_source = "$elem_dir$else.xcms";
    if(!file_exists(@$then_source)) @$then_source = "$elem_dir${then}default.xcms";
    if(!file_exists(@$else_source)) @$else_source = "$elem_dir${else}default.xcms";
    // damn, nothing suits
    if(!file_exists(@$then_source)) @$then_source = "$elem_dir$then.code";
    if(!file_exists(@$else_source)) @$else_source = "$elem_dir$else.code";

    @$then_dest = $SETTINGS["precdir"].str_replace('/', '_', $then_source).".php";
    @$else_dest = $SETTINGS["precdir"].str_replace('/', '_', $else_source).".php";

    compile($then_source, $then_dest);
    if (@$else && $else != "NULL") compile($else_source, $else_dest);

    setArgs(@$input[4], $outputStream);
    fputs($outputStream,
        '<'.'?php '.
        "if($cond) { include('$then_dest'); } ");
    if (@$else && $else !="NULL")
        fputs($outputStream, "else { include('$else_dest'); }");

    fputs($outputStream, '?'.'>');
?>
