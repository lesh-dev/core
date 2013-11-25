<?php
    $input = explode(EXP_SL2, $code);
    foreach ($input as $key=>$value)
        $input[$key] = str_replace(EXP_SL2, '', $value);

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

    xcms_compile($then_source, $then_dest);
    if (@$else && $else != "NULL")
        xcms_compile($else_source, $else_dest);

    xcms_set_args(@$input[4], $output_stream);
    fputs($output_stream,
        '<'.'?php '.
        "if($cond) { include('$then_dest'); } ");
    if (@$else && $else !="NULL")
        fputs($output_stream, "else { include('$else_dest'); }");

    fputs($output_stream, '?'.'>');
?>
