<?php 
/* version 1.2.1. editlist_form list of skipping fields added*/  
/* version 1.2. function editlist_form - a gui editor for lists.*/  
/* version 1.1. _defend tag in the beginning added.
   Now, if file is handled as php script, user will 
   not read it. */  
/* version 1.0. Library created */  

/********************************/
/*          SETTINGS            */
/**/$tag_php_delim = "<###>"; /**/
/********************************/
  function applyTag($str,$list,$prefix="<",$suffix=">")
  {
    $s = $str;
    foreach ($list as $key=>$value) 
    {
      $s = str_replace($prefix.$key.$suffix,$value,$s);	
    }  
    return $s;  
  }
  
  function saveList($list,$filename)
  {
    global $tag_php_delim;
    $f = fopen($filename,"w");
    
    $rez = "_defend".$tag_php_delim."<?php die(); ?".'>'."\n";
    fputs($f,$rez);
    
    foreach ($list as $key=>$value) 
    {
      if($key=="") continue;
      if($key[0]=='_') continue;
      $rez = $key.$tag_php_delim.$value."\n";
      fputs($f,$rez);
    }
    fclose($f);  
  }
  
  function getList($filename)
  {
    global $tag_php_delim;
    $s = file($filename);
    foreach ($s as $key=>$value) 
    {
      $v = str_replace("\n","",$value);
      $v = str_replace("\r","",$v);
      $k = explode($tag_php_delim, $v, 2);
      if($k[0] == "_defend") continue;
      @$rez[$k[0]] = @$k[1];	
    }
    return $rez;
  }
  
  function editlist_form($file, $addparams,$skipparams="")
  {
    $list = getList($file);
    if(!$list) echo "bad filename!";

    if(@$_POST["editTag"])
    {
      foreach ($_POST as $key=>$value) {
      	if(strstr($key,"edtg_"))
        {
          $list[substr($key, "5")] = $value;
        }
      }
      if(@$_POST["newkey"])
      {
        $list[$_POST["newkey"]] = @$_POST["newvalue"];
      }
      saveList($list,$file);
      $list = getList($file);
      
    }

    echo '<form action="'.$addparams.'" method="post"><table><tr><td><b>Ключ</b><td><b>Значение</b>';
    foreach ($list as $key=>$value) 
    {
      if(!strstr($skipparams,$key)) 
        echo "<tr><td>$key<td><input name=\"edtg_$key\" value=\"$value\">";	
    }
    echo "<tr><td><input name=\"newkey\"><td><input name=\"newvalue\">";	
    echo "</table>";    
    //echo $addparams;
    echo '<input type="submit" name="editTag" value="Изменить">';    
    echo '</form>';
  }
  
?>
