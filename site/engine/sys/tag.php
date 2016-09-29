<?php

require_once("${engine_dir}sys/string.php");

define('XCMS_TAG_NAME', "_NAME");

function xcms_enable_key(&$list, $key)
{
    $list[$key] = XU_YES;
}

function xcms_disable_key(&$list, $key)
{
    $list[$key] = XU_NO;
}

function xcms_is_enabled_key($list, $key, $default = false)
{
    if (!array_key_exists($key, $list))
        return $default;
    return ($list[$key] == XU_YES);
}

function xcms_is_disabled_key($list, $key, $default = false)
{
    if (!array_key_exists($key, $list))
        return $default;
    return ($list[$key] != XU_YES);
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
        xcms_log(XLOG_ERROR, "[STORAGE] List file '$file' cannot be found");
        return $keys;
    }
    $cont = file($file);
    foreach ($cont as $line)
    {
        $line = trim($line);
        $p = strpos($line, ':');
        if ($p === false)
        {
            xcms_log(XLOG_WARNING, "[STORAGE] Invalid line in file '$file': '$line'");
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
    $output = "";
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
        $output .= "$key:$value\n";
    }
    if (!xcms_write($file, $output))
    {
        xcms_log(XLOG_ERROR, "[STORAGE] Cannot open list file '$file' for writing");
        return false;
    }
    return true;
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
    global $SETTINGS;
    $file = "{$SETTINGS["engine_dir"]}taglist/$tag_name";
    return file_exists($file);
}

function xcms_get_tag_list($tag_name)
{
    global $SETTINGS;
    $tag_file_name = "{$SETTINGS["engine_dir"]}taglist/$tag_name";
    $tag_text = file_get_contents($tag_file_name);
    $tag_text = str_replace("\r", "", $tag_text);

    if (substr($tag_text, 0, 5) != "<?php")
    {
        $rez = explode(EXP_LF, $tag_text);
        foreach ($rez as $key => $value)
        {
            if (!$key)
            {
                $taglist[XCMS_TAG_NAME] = $value;
                continue;
            }
            $arr = explode(EXP_EQ, $value);
            $taglist[trim($arr[0])] = trim($arr[1]);
        }
        return $taglist;
    }
    else
    {
        $taglist = array();
        include($tag_file_name);
        $taglist[XCMS_TAG_NAME] = $tagname;
        return $taglist;
    }
}

function xcms_draw_text_tag($id, $value, $is_longtext, $placeholder = "")
{
    if ($is_longtext)
    {
        $text_value = str_replace("|", "\n", $value);
        ?>
        <textarea
            name="<?php echo $id; ?>"
            id="<?php echo $id; ?>"
            placeholder="<?php echo htmlspecialchars($placeholder); ?>"
            class="key-value"
            rows="5"
            ><?php echo htmlspecialchars($text_value); ?></textarea><?php
    }
    else
    {?>
        <input
            name="<?php echo $id; ?>"
            id="<?php echo $id; ?>"
            placeholder="<?php echo htmlspecialchars($placeholder); ?>"
            value="<?php echo htmlspecialchars($value); ?>"
            class="key-value" /><?php
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
    $list = xcms_get_list($file);

    if (@$_POST["edit_tag"])
    {
        foreach ($_POST as $key => $value)
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
    foreach ($list as $key => $value)
    {
        if (strstr($skip_params, $key))
            continue;

        $id = "edtg_$key";
        if (xcms_tag_exists($key))
        {
            $taglist = xcms_get_tag_list($key); ?>

            <tr><td><?php echo $taglist[XCMS_TAG_NAME]; ?></td><td><?php

            if (count($taglist) > 1)
            {?>

                <select name="<?php echo $id; ?>" id="<?php echo $id; ?>" class="key-value"><?php
                foreach ($taglist as $vtag => $tag)
                {
                    if ($vtag == XCMS_TAG_NAME) continue;
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
        <p>Для удаления поля введите <b>_FORGET</b> в его значение</p>
        <?php xcmst_submit("edit_tag", "Сохранить"); ?>
    </form><?php
}

/**
  * Key-Value module unit test
  **/
function xcms_keyvalue_unit_test()
{
    xut_begin("keyvalue");

    $values = array();
    $values["key1"] = " value 1\n\r";
    $values["key2 "] = " value\r2   ";
    $values["key 3 "] = "proper-value-without-spaces";
    $values[" key-4 "] = "proper-value-without-spaces";
    $values[" key\n5 "] = "proper\nvalue\rwithout\r\nspaces";
    $values[" key6 "] = "proper\nvalue\rwithout\r\nspaces";
    $values[" key7 "] = "generic  values  with   lots  of spaces";
    $values_count = count($values);
    global $SETTINGS;
    xut_check(xcms_save_list("${SETTINGS["content_dir"]}test-list", $values), "List save");
    $read_values = xcms_get_list("${SETTINGS["content_dir"]}test-list");
    xut_equal($values_count, count($read_values), "Invalid test values count");

    $check["key1"] = "value 1";
    $check["key2"] = "value 2";
    $check["key 3"] = "proper-value-without-spaces";
    $check["key-4"] = "proper-value-without-spaces";
    $check["key 5"] = "proper value without  spaces";
    $check["key6"] = "proper value without  spaces";
    $check["key7"] = "generic  values  with   lots  of spaces";
    xut_equal($values_count, count($check), "Invalid check values count");

    foreach ($read_values as $key => $value)
    {
        $cv = xcms_get_key_or($check, $key, "INVALID");
        xut_check($cv != "INVALID", "Invalid value received");
        xut_equal($value, $cv, "Values do not match");
    }

    xut_end();
}

?>
