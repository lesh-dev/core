<?php
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
        // keys are cleaned from non-printing chars
        $key = str_replace("\r", " ", $key);
        $key = str_replace("\n", " ", $key);
        $key = str_replace("\t", " ", $key);
        $key = trim($key);
        $value = str_replace("\r", " ", $value);
        $value = str_replace("\n", " ", $value);
        $value = trim($value);

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
    // special case for bool vars
    if (is_bool($def_value))
        return $value;

    if (!strlen($value))
        return $def_value;
    return $value;
}

/**
  * For internal usage only
  **/
function xcms_convert_multiline($value)
{
    // handle windows
    $value = str_replace("\r\n", "|", $value);
    // linux
    $value = str_replace("\n", "|", $value);
    // and old MacOS
    $value = str_replace("\r", "|", $value);
    return $value;
}


function xcms_tag_exists($tag_name)
{
    $file = "{$SETTINGS["engine_dir"]}taglist/$tag_name";
    return file_exists($file);
}

function xcms_get_tag_list($tag_name)
{
    $file = "{$SETTINGS["engine_dir"]}taglist/$tag_name";
    $filec = file_get_contents($file);
    $filec = str_replace("\r", "", $filec);
    if(substr($filec, 0, 5) != "<?php")
    {
        $rez = explode("\n", $filec);
        foreach($rez as $key=>$value)
        {
            if(!$key)
            {
                $taglist["_NAME"]=$value;
                continue;
            }
            $arr = explode("=", $value);
            $taglist[trim($arr[0])] = trim($arr[1]);
        }
        return $taglist;
    }
    else
    {
        $taglist = array();
        include($file);
        $taglist["_NAME"] = $tagname;
        return $taglist;
    }
}

/**
  * deprecated function, do not use
  **/
function saveList($list, $filename)
{
    global $tag_php_delim;
    $f = fopen($filename, "w");

    $rez = "_defend".$tag_php_delim."<?php die(); ?".'>'."\n";
    fputs($f, $rez);

    foreach ($list as $key=>$value)
    {
        if($key=="") continue;
        if($key[0]=='_') continue;
        $rez = $key.$tag_php_delim.$value."\n";
        fputs($f, $rez);
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
        $v = str_replace("\n", "", $value);
        $v = str_replace("\r", "", $v);
        $k = explode($tag_php_delim, $v, 2);
        if($k[0] == "_defend") continue;
        @$rez[$k[0]] = @$k[1];
    }
    return $rez;
}


function xcms_draw_text_tag($id, $value, $is_longtext, $placeholder = "")
{
    if ($is_longtext)
    {
        $text_value = str_replace("|", "\n", $value);
        ?>
        <textarea name="<?php echo $id; ?>" id="<?php echo $id; ?>"
            placeholder="<?php echo htmlspecialchars($placeholder); ?>"
            class="key-value" ><?php echo htmlspecialchars($text_value); ?></textarea><?php
    }
    else
    {?>
        <input name="<?php echo $id; ?>" id="<?php echo $id; ?>"
            placeholder="<?php echo htmlspecialchars($placeholder); ?>"
            value="<?php echo htmlspecialchars($value); ?>" class="key-value" /><?php
    }
}

/**
  * WARNING: This function contains deprecated code
  * flags:
  * no-new-key - disable new key addition (not used in XCMS now)
  * longtext - use textareas instead of text input
  **/
function xcms_editlist_form($file, $skip_params = "", $flags = "")
{
    global $SETTINGS;
    $list = xcms_get_list($file);

    if (@$_POST["editTag"])
    {
        foreach ($_POST as $key=>$value)
        {
            $key_name = substr($key, 5);
            if ($value == "_FORGET" || $value == "__FORGET")
            {
                unset($list[$key_name]);
                continue;
            }
            if (strstr($key, "edtg_"))
                $list[$key_name] = xcms_convert_multiline($value);
        }

        if (!strstr($flags, "no-new-key") && @$_POST["newkey"])
            $list[$_POST["newkey"]] = xcms_convert_multiline(xcms_get_key_or($_POST, "newvalue"));

        xcms_save_list($file, $list);
        $list = xcms_get_list($file);
    }
    $is_longtext = (strstr($flags, "longtext") !== false);

    ?>

    <form action="" method="post">
        <table class="key-value"><?php
    foreach ($list as $key=>$value)
    {
        if (strstr($skip_params, $key))
            continue;

        $id = "edtg_$key";
        if (xcms_tag_exists($key))
        {
            $taglist = xcms_get_tag_list($key); ?>

            <tr><td><?php echo $taglist["_NAME"]; ?></td><td><?php

            if (count($taglist) > 1)
            {?>

                <select name="<?php echo $id; ?>" id="<?php echo $id; ?>" class="key-value"><?php
                foreach ($taglist as $vtag=>$tag)
                {
                    if ($vtag == "_NAME") continue;
                    $vtag = htmlspecialchars($vtag);
                    $tag = htmlspecialchars($tag);
                    if ($tag == $value) echo "<option selected value=\"$tag\">$vtag</option>";
                    else echo "<option value=\"$tag\">$vtag</option>";
                }
                echo "</select>";
            }
            else
                xcms_draw_text_tag($id, $value, $is_longtext); ?>

            </td></tr>
            <?php
        }
        else
        {?>
            <tr><td><?php echo $key; ?></td><td><?php
            xcms_draw_text_tag($id, $value, $is_longtext); ?>
            </td></tr><?php
        }
    }
    if (!strstr($flags, "no-new-key"))
    {?>
        <tr>
            <td><input name="newkey" id="newkey"
                class="key-name" placeholder="Новое поле" ></td>
            <td><?php
                xcms_draw_text_tag("newvalue", "", $is_longtext, "Новое значение");
            ?></td>
        </tr><?php
    }
    ?>
        </table>
        <input type="submit" name="editTag" id="editTag" value="Сохранить" />
    </form><?php
}

function xcms_keyvalue_unit_test()
{
    xut_begin("keyvalue");
    // first of all, test xcms_get_key_or function
    $obj = array();
    $obj["super"] = 1;
    $obj["pupper"] = false;
    $obj["zero-value"] = 0;
    $obj["another"] = "test string";
    $obj["empty"] = "";

    xut_check(1 === xcms_get_key_or($obj, "super"), "Invalid 'super' key");
    xut_check(false === xcms_get_key_or($obj, "pupper", true), "Invalid 'pupper' key");
    xut_check(0 === xcms_get_key_or($obj, "zero-value"), "Invalid 'zero-value' key");
    xut_check("test string" === xcms_get_key_or($obj, "another"), "Invalid 'another' key");
    xut_check("" === xcms_get_key_or($obj, "empty"), "Invalid 'empty' key");
    xut_check("some" === xcms_get_key_or($obj, "empty", "some"), "Failed empty value key test");
    xut_check("" === xcms_get_key_or($obj, "missing"), "Failed missing key test");
    xut_check(true === xcms_get_key_or($obj, "missing-bool", true), "Failed missing bool key");
    xut_check(false === xcms_get_key_or($obj, "pupper", true), "Failed existing bool key");

    $values = array();
    $values["key1"] = " value 1\n\r";
    $values["key2 "] = " value\r2   ";
    $values["key 3 "] = "proper-value-without-spaces";
    $values[" key-4 "] = "proper-value-without-spaces";
    $values[" key\n5 "] = "proper\nvalue\rwithout\r\nspaces";
    $values[" key6 "] = "proper\nvalue\rwithout\r\nspaces";
    $values[" key7 "] = "generic  values  with   lots  of spaces";
    global $SETTINGS;
    xut_check(xcms_save_list("${SETTINGS["datadir"]}test-list", $values), "List save");
    $read_values = xcms_get_list("test-list");

    $check["key1"] = "value 1";
    $check["key2"] = "value 2";
    $check["key 3"] = "proper-value-without-spaces";
    $check["key-4"] = "proper-value-without-spaces";
    $check["key 5"] = "proper value without  spaces";
    $check["key6"] = "proper value without  spaces";
    $check["key7"] = "generic  values  with   lots  of spaces";

    foreach ($read_values as $key => $value)
    {
        $cv = xcms_get_key_or($check, $key, "INVALID");
        xut_check($cv != "INVALID", "Invalid value received");
        xut_check($value == $cv, "Values do not match");
    }

    xut_end();
}

?>
