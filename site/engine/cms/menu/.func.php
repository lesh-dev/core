<?php
/*  $html_array = glob("*.html");

  function sort_by_mtime($file1,$file2) {
     $time1 = filemtime($file1);
     $time2 = filemtime($file2);
     if ($time1 == $time2) {
         return 0;
     }
     return ($time1 < $time2) ? 1 : -1;
     }

usort($html_array,"sort_by_mtime");
//$html_array is now ordered by the time it was last modified
*/
?>

<?php
  function cms_menu_make($initPath,$MENUTEMPLATES,$menuLevel,$addhrefparams,$options,$startLevel,$endLevel)
  {
    global $SETTINGS,$forceSn,$pageid,$login,$group,$web_prefix;    
    $pageiid = str_replace("{$SETTINGS["datadir"]}cms/pages/","",$initPath);
    $flags="";
    if(!file_exists("$initPath/applymenu")) 
    {
      if(strstr($options,"+displayall"))
        $text = "{unnamed}";
      else
        return;
    }
    
    else if(file_exists("$initPath/lockmenu"))
    {
      if(strstr($options,"+displayall"))
      {
        $flags.="H ";
        $text = file_get_contents("$initPath/applymenu");
      }
      else
        return;
    }
    else if(file_exists("$initPath/hidemenu"))
    {      
      if(strstr($options,"+displayall"))
        $text = file_get_contents("$initPath/applymenu");
      else
      {
        $INFO = @getList("$initPath/info");
        include(translate("<! auth/lauth {$INFO['view']} !>"));        
        if($acsess)
          $text = file_get_contents("$initPath/applymenu");
        else return;
      }
    }
    else 
      $text = file_get_contents("$initPath/applymenu");
    
    //echo "<br>*".$pageid."#<br>";
    
    $html = $MENUTEMPLATES[$menuLevel];
    if(strstr($options,"+devel"))
    {
      $margin = $menuLevel*10;
      $html = "<br><a style=\"margin-left: {$margin}pt;\" href=\"<HREF>\">[$flags<TEXT>]</a>";
      $html = str_replace("<HREF>","/$web_prefix?page=$pageiid&$addhrefparams",$html);
    }
    else if(file_exists("$initPath/currtag"))
    {
	$tag = file_get_contents("$initPath/currtag");
	$html = str_replace("<HREF>","/$web_prefix$tag/$addhrefparams",$html);
    }
    else
	$html = str_replace("<HREF>","/$web_prefix?page=$pageiid&$addhrefparams",$html);
    $html = str_replace("<TEXT>",$text,$html);
    
    if(strstr($pageid,str_replace("{$SETTINGS["datadir"]}cms/pages/","",$initPath)))
      $html = str_replace("<ACTIVE>","active",$html);
    else
      $html = str_replace("<ACTIVE>","passive",$html);
      
    if(file_exists("$initPath/menuicon.gif"))
    {
      $html = str_replace("<!-- PIC -->","<img border=\"0\" src=\"$initPath/menuicon.gif\"><br>",$html);
    }
    if($forceSn) $html = "<tr>".$html;
    if($menuLevel>=$startLevel && $menuLevel<=$endLevel)
    {
      echo $html;
    }
    $array = glob("$initPath/*",GLOB_ONLYDIR);
    if(!strstr($options,"+hault"))
      if(@$array) foreach ($array as $key=>$value) 
      {
        if(strstr($options,"+devel") || strstr($pageid,str_replace("{$SETTINGS["datadir"]}cms/pages/","",$value)))
          cms_menu_make($value,$MENUTEMPLATES,$menuLevel+1,$addhrefparams,$options,$startLevel,$endLevel);
        else
          cms_menu_make($value,$MENUTEMPLATES,$menuLevel+1,$addhrefparams,$options."+hault",$startLevel,$endLevel);
      }
  }
?>
