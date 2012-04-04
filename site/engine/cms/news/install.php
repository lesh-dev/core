<?php
  $LIST["installed"] = "ok";
  $LIST["maxNews"] = 10;
  $INFO["installed"] = "ok";
  $INFO["maxNews"] = 10;
  saveList($INFO,"{$SETTINGS["datadir"]}cms/pages/$pageid/info");
  $f = fopen("{$SETTINGS["datadir"]}cms/pages/$pageid/template","w");
  fputs($f,
'
  <div class="newstitle"><a href="<STAMP>"><DATE>. Header</a></div>
    <p class="text">text</p>
  <div class="signature"><LOGIN></div>
'
  );
  fclose($f);
  //saveList($LIST,"{$SETTINGS["datadir"]}cms/pages/$pageid/info");
  //echo '<script>alert("раздел новостей '.$pageid.' создан и инициализирован.");</script>';
  
?>
