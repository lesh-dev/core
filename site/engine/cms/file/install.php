<?php
  $LIST["installed"] = "ok";
  $LIST["immidiate"] = "false";
  
  $f = fopen("{$SETTINGS["datadir"]}cms/pages/$pageid/lockmenu","w");
  fputs($f,"true");
  fclose($f);
  
?>