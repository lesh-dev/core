<?php
  $html_array = glob("*.html");

  function sort_by_mtime($file1,$file2) {
     $time1 = filemtime($file1);
     $time2 = filemtime($file2);
     if ($time1 == $time2) {
         return 0;
     }
     return ($time1 < $time2) ? 1 : -1;
     }

  if (! empty($html_array))
     usort($html_array,"sort_by_mtime");
//$html_array is now ordered by the time it was last modified
?>

<?
  function cms_menu_make($initPath,$MENUTEMPLATES,$menuLevel,$addhrefparams,$options,$startLevel,$endLevel)
  {
    global $SETTINGS,$forceSn,$pageid;    
    $pageiid = str_replace("{$SETTINGS["datadir"]}cms/pages/","",$initPath);
    
    if(!file_exists("$initPath/applymenu")) 
    {
      if(strstr($options,"+displayall"))
        $text = "{unnamed}";
      else
        return;
    }
    else 
      $text = file_get_contents("$initPath/applymenu");
    
    //echo "<br>*".$pageid."#<br>";
    
    $html = $MENUTEMPLATES[$menuLevel];
    $html = str_replace("<HREF>","?page=$pageiid&amp;$addhrefparams",$html);
    $html = str_replace("<TEXT>",$text,$html);
    
    if(strstr($pageid,str_replace("data/cms/pages/","",$initPath)))
      $html = str_replace("<ACTIVE>","active",$html);
    else
      $html = str_replace("<ACTIVE>","inactive",$html);
      
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
        if(strstr($pageid,str_replace("data/cms/pages/","",$value)))
        //echo "<br>$pageid ^^ $value<br>";
          cms_menu_make($value,$MENUTEMPLATES,$menuLevel+1,$addhrefparams,$options,$startLevel,$endLevel);
        else
          cms_menu_make($value,$MENUTEMPLATES,$menuLevel+1,$addhrefparams,$options."+hault",$startLevel,$endLevel);
      }
  }
?>
