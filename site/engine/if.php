<?php
  $input = explode("//",$code);
  foreach ($input as $key=>$value) {
  	$input[$key] = str_replace("//","",$value);
  }

  @$source1 = "{$SETTINGS["elementsdir"]}{$input[2]}.xcms";
  @$source2 = "{$SETTINGS["elementsdir"]}{$input[3]}.xcms";
  if(!file_exists(@$source1)) @$source1 = "{$SETTINGS["elementsdir"]}{$input[2]}.code";
  if(!file_exists(@$source2)) @$source2 = "{$SETTINGS["elementsdir"]}{$input[3]}.code";
  @$dest1 = $SETTINGS["precdir"].str_replace("/","_",$source1).".php";
  @$dest2 = $SETTINGS["precdir"].str_replace("/","_",$source2).".php";

  compile($source1,$dest1);
  if(@$input[3]) if(@$input[3]!="NULL") compile($source2,$dest2);

  setArgs(@$input[4],$outputStream);
  fputs($outputStream,
  "<"."?php ".
  "if({$input[1]}){include('$dest1');} ");

  if(@$input[3]) if(@$input[3]!="NULL") fputs($outputStream,"else {include('$dest2');}");

  fputs($outputStream,"?".">");
?>
