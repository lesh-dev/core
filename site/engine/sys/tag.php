<?php
/* version 1.4. rewritten from scratch [mvel@] */

/* version 1.3   added taglist system. Afraid, this makes tags depending of xcms.*/
/* version 1.2.1. editlist_form list of skipping fields added*/
/* version 1.2. function editlist_form - a gui editor for lists.*/
/* version 1.1. _defend tag in the beginning added.
   Now, if file is handled as php script, user will
   not read it. */
/* version 1.0. Library created */


/**
  * Retrieve current page content location
  * Assumes @name pageid and @name SETTINGS are defined
  * TODO: Should be placed in the proper file (cms-related)
  **/
function xcms_get_info_file_name()
{
    global $SETTINGS;
    global $pageid;
    return "{$SETTINGS["datadir"]}cms/pages/$pageid/info";
}

/**
  * Retrieves key-value-stored list from file
  * @param file file name to read from
  * @return key-value array with values (or empty array
  * in case of errors)
  **/
function xcms_get_list($file)
{
    $keys = array();
    if (!file_exists($file))
    {
        xcms_log(0, "List file '$file' cannot be found");
        return $keys;
    }
    $cont = file($file);
    foreach ($cont as $line)
    {
        $line = trim($line);
        $p = strpos($line, ':');
        if ($p === false)
        {
            xcms_log(1, "Invalid line in file '$file': '$line'");
            continue;
        }
        $key = substr($line, 0, $p);
        $value = substr($line, $p + 1);
        // TODO: key regexp filtering
        $keys[$key] = $value;
    }
    return $keys;
}

// TODO: document doxygen code style
/**
  *  Writes key-value array to file
  *  @param file file name
  *  @return true on success write, false otherwise
  **/
function xcms_save_list($file, $keys)
{
    $f = @fopen($file, "w");
    if (!$f)
    {
        xcms_log(0, "Cannot open list file '$file' for writing");
        return false;
    }
    foreach ($keys as $key => $value)
    {
        $value = trim($value);
        $value = str_replace("\r", " ", $value);
        $value = str_replace("\n", " ", $value);
        $value = str_replace("  ", " ", $value);

        // TODO: write error handling
        fwrite($f, "$key:$value\n");
    }
    fclose($f);
    return true;
}

/**
  * This function typically should not be used. Instead,
  * you should read all the keys and use them if possible
  * to prevent duplicated disk access.
  **/
function xcms_get_key($file, $key)
{
    $keys = xcms_get_list($file);
    if (array_key_exists($key, $keys))
        return $keys[$key];
    return NULL;
}

/********************************/
/*          SETTINGS            */
/**/$tag_php_delim = "<###>"; /**/
/********************************/
  function getTagList($file)
  {
  	global $getTagList_output;
	$filec = file_get_contents($file);
	$filec = str_replace("\r","",$filec);
	if(substr($filec,0,5) != "<?php")
	{
		$rez = explode("\n",$filec);
		foreach($rez as $key=>$value)
		{
			if(!$key)
			{
				$taglist["_NAME"]=$value;
				continue;
			}
			$arr = explode("=",$value);
			$taglist[$arr[0]]=$arr[1];
		}
		return $taglist;
	}
	else
	{
		$taglist = array();
		include($file);
		$getTagList_output = $tagname;
		$taglist["_NAME"]=$tagname;
		return $taglist;
	}
  }
/*
  function applyTag($str,$list,$prefix="<",$suffix=">")
  {
    $s = $str;
    foreach ($list as $key=>$value)
    {
      $s = str_replace($prefix.$key.$suffix,$value,$s);
    }
    return $s;
  }
*/
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
    $rez = array();
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

  function editlist_form($file, $addparams, $skipparams="",$securityflags="")
  /**
   * secyrityflags:
   *   -newkey - disable newkey option
  **/
  {
    global $SETTINGS;
    $list = xcms_get_list($file);
    if(!$list) echo "bad filename!";

    if(@$_POST["editTag"])
    {
      foreach ($_POST as $key=>$value) {
        if($value == "_FORGET") {unset($list[substr($key, "5")]); continue;}
        if($value == "__FORGET") {unset($list[substr($key, "5")]); continue;}
      	if(strstr($key,"edtg_"))
        {
          //if($list[substr($key, "5")])
          {
            $list[substr($key, "5")] = stripslashes($value);
          }
        }
      }
      if(@$_POST["newkey"])
      {
	if(strstr($securityflags,"-newkey")){}
        else $list[$_POST["newkey"]] = @$_POST["newvalue"];
      }
      saveList($list,$file);
      $list = getList($file);
    }

    echo '<form action="'.$addparams.'" method="post"><table>';
    foreach ($list as $key=>$value)
    {
      if(!strstr($skipparams,$key))
      {
      	if(file_exists("{$SETTINGS["elementsdir"]}taglist/$key"))
      	{
      		$getTagList_output = "sss";
      		$taglist = getTagList("{$SETTINGS["elementsdir"]}taglist/$key");
	      	echo "<tr><td>".$taglist["_NAME"]."<td>";
	      	if(count($taglist)>1)
	      	{
			echo "<SELECT name=edtg_$key>";
			foreach($taglist as $vtag=>$tag)
			{
				if($vtag == "_NAME") continue;
				//$tag = str_replace("\n","",$tag);
				//$tag = str_replace("\r","",$tag);
				if($tag == $value)	echo "<OPTION selected value=\"$tag\">$vtag</OPTION>";
				else			echo "<OPTION          value=\"$tag\">$vtag</OPTION>";
			}
			echo "</SELECT>";
		}
		else
			echo "<input name=\"edtg_$key\" value=\"$value\">";
      	}
        else
        {
	      	echo "<tr><td>$key<td>";
        	echo "<input name=\"edtg_$key\" value=\"$value\">";
        }
      }
    }
    if(strstr($securityflags,"-newkey")){}
    else
    	echo "<tr><td><input name=\"newkey\" placeholder=\"Новое поле\"><td><input name=\"newvalue\" placeholder=\"Новое значение\">";

    echo "</table>";
    //echo $addparams;
    echo '<input type="submit" name="editTag" value="Save">';
    echo '</form>';
  }

?>
