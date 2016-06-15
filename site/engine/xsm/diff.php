<?php

include_once("$engine_dir/sys/diff/diff-utils.php");

/**
  * Нормализация и прочистка массивов перед сравнением
  **/
function xcms_normalize_array($arr, $table_name, $fields)
{
    $anew = array();
    foreach ($arr as $key => $value)
    {
        if (!array_key_exists($key, $fields))
            continue;

        if ($key == "${table_name}_created")
            continue;

        if ($key == "${table_name}_modified")
            continue;

        $value = trim($value);
        $value = str_replace(EXP_CRLF, EXP_LF, $value);
        $value = str_replace(EXP_CR, EXP_LF, $value);
        $anew[$key] = $value;
    }
    return $anew;
}

/**
  * Построение разности двух key-массивов
  **/
function xcms_array_diff($new, $old, $table_name, $fields)
{
    $new = xcms_normalize_array($new, $table_name, $fields);
    $old = xcms_normalize_array($old, $table_name, $fields);

    $diff = array();
    foreach ($new as $key => $value)
    {
        if (!array_key_exists($key, $old))
        {
            if (strlen($value))
                $diff[] = array('key'=>$key, 'new'=>$value, 'old'=>'');
            continue;
        }
        // key exists in both arrays
        if ($old[$key] != $value)
            $diff[] = array('key'=>$key, 'new'=>$value, 'old'=>$old[$key]);
    }
    foreach ($old as $key => $old_value)
    {
        if (array_key_exists($key, $new))
            continue;
        if (strlen($old_value))
            $diff[] = array('key'=>$key, 'new'=>'', 'old'=>$old_value);
    }
    return $diff;
}

/**
  * Build a diff message of two objects in html format.
  * @return HTML-message or empty string if objects are equal.
  **/
function xsm_build_diff_msg($new_object, $old_object, $table_name, $fields, $table_title)
{
    $mail_msg = xcms_get_html_template("xsm-diff-message");
    $row_template = xcms_get_html_template("xsm-row-finediff");

    $non_empty_old = (count($old_object) != 0);
    $diff_array = xcms_array_diff($new_object, $old_object, $table_name, $fields);
    if (count($diff_array) == 0)
        return "";

    $content = ""; // @@TABLE-CONTENT@
    foreach ($diff_array as $diff)
    {
        $key = $diff['key'];
        $desc = $fields[$key];
        $key_title = $desc["name"];
        $ft = xcms_get_key_or($desc, "type");
        $old_value = $diff['old'];
        $new_value = $diff['new'];
        $cur_row = $row_template;
        if ($ft == "checkbox")
        {
            if (xu_empty($old_value))
            {
                if ($non_empty_old)
                    $old_value = "Нет";
            }
            else
                $old_value = "Да";
            $new_value = xu_not_empty($new_value) ? "Да" : "Нет";
        }
        if (xsm_enum_exists($key))
        {
            $enum_items = xsm_get_enum($key);
            if (xu_empty($old_value))
            {
                if ($non_empty_old)
                {
                    // see #910: show only diffs
                    $old_value = xsm_get_enum_default_value($key);
                    $old_value = $enum_items[$old_value];
                }
            }
            else
                $old_value = $enum_items[$old_value];
            $new_value = $enum_items[$new_value];
        }

        $cur_row = str_replace("@@KEY@", $key_title, $cur_row);
        $diff_html = xcms_diff_html($old_value, $new_value);
        $cur_row = str_replace("@@DIFF@", $diff_html, $cur_row);
        $content .=  $cur_row;
    }
    $content = xcms_wrap_long_lines($content);

    $mail_msg = str_replace("@@TABLE-CONTENT@", $content, $mail_msg);
    $mail_msg = str_replace("@@TABLE-TITLE@", $table_title, $mail_msg);

    return $mail_msg;
}
