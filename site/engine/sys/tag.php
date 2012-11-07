<?php
/*
    version 1.4. rewritten from scratch [mvel@]
    version 1.3   added taglist system. Afraid, this makes tags depending of xcms.
    version 1.2.1. editlist_form list of skipping fields added
    version 1.2. function editlist_form - a gui editor for lists.
    version 1.1.
        _defend tag in the beginning added.
        Now, if file is handled as php script, user will
        not read it.
    version 1.0. Library created
*/

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
  * Makes checkbox checked attribute with proper generic value
  **/
function xcms_checkbox_attr($val)
{
    $attr = ' value="yes" ';
    if ($val == "yes")
        $attr .= ' checked="checked" ';
    return $attr;
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
        $key = trim(substr($line, 0, $p));
        $value = trim(substr($line, $p + 1));
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
  * Gey key value from list or return default value
  **/
function xcms_get_key_or($list, $key, $def_value = '')
{
    if (!array_key_exists($key, $list))
        return $def_value;
    $value = $list[$key];
    if (!strlen($value))
        return $def_value;
    return $value;
}

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

/**
  * deprecated function, do not use
  **/
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

/**
  * deprecated function, do not use
  **/
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

/**
  * WARNING: This function contains deprecated code
  * secyrityflags:
  * -newkey - disable newkey option
  **/
function editlist_form($file, $addparams, $skipparams="",$securityflags="", $old_mode=false)
{
    global $SETTINGS;
    if ($old_mode) $list = getList($file);
    else $list = xcms_get_list($file);

    if(@$_POST["editTag"])
    {
        foreach ($_POST as $key=>$value)
        {
            if($value == "_FORGET")
            {
                unset($list[substr($key, "5")]);
                continue;
            }
            if($value == "__FORGET")
            {
                unset($list[substr($key, "5")]);
                continue;
            }
            if(strstr($key,"edtg_"))
            {
                $list[substr($key, "5")] = stripslashes($value);
            }
        }
        if(@$_POST["newkey"])
        {
            if(!strstr($securityflags,"-newkey"))
                $list[$_POST["newkey"]] = @$_POST["newvalue"];
        }
        if ($old_mode)
        {
            saveList($list, $file);
            $list = getList($file);
        }
        else
        {
            xcms_save_list($file, $list);
            $list = xcms_get_list($file);
        }
    }
    ?>

    <form action="<?php echo $addparams; ?>" method="post">
        <table class="key-value"><?php
    foreach ($list as $key=>$value)
    {
        if (strstr($skipparams, $key))
            continue;

        $id = "edtg_$key";
        if(file_exists("{$SETTINGS["engine_dir"]}taglist/$key"))
        {
            $getTagList_output = "sss";
            $taglist = getTagList("{$SETTINGS["engine_dir"]}taglist/$key");
            echo "<tr><td>".$taglist["_NAME"]."</td><td>";
            if(count($taglist)>1)
            {?>
                <select name="<?php echo $id; ?>" id="<?php echo $id; ?>" class="key-value"><?php
                foreach($taglist as $vtag=>$tag)
                {
                    if($vtag == "_NAME") continue;
                    if($tag == $value) echo "<option selected value=\"$tag\">$vtag</option>";
                    else echo "<option value=\"$tag\">$vtag</option>";
                }
                echo "</select>";
            }
            else
            {?>
                <input name="<?php echo $id; ?>" id="<?php echo $id; ?>"
                    value="<?php echo $value; ?>" class="key-value" /><?php
            }?>
            </td></tr>
            <?php
        }
        else
        {?>
            <tr><td><?php echo $key; ?></td><td>
                <input name="<?php echo $id; ?>" id="<?php echo $id; ?>"
                    value="<?php echo $value; ?>" class="key-value" />
            </td></tr><?php
        }
    }
    if (!strstr($securityflags,"-newkey"))
    {?>
        <tr>
            <td><input name="newkey" id="newkey"
                class="key-name" placeholder="Новое поле" ></td>
            <td><input name="newvalue" id="newvalue"
                class="key-value" placeholder="Новое значение"></td>
        </tr><?php
    }
    ?>
        </table>
        <input type="submit" name="editTag" id="editTag" value="Сохранить" />
    </form><?php
}

?>
