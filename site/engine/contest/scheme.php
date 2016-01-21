<?php

$CONTEST_CURRENT_YEAR = "2015";

define('CTX_NO_SOLUTION', '-');
define('CTX_STOLEN_SOLUTION', 'stolen');
define('CTX_STOLEN_SOLUTION_HT', '<b style="color: #ff0000">Списана</b>');
define('CTX_NO_SOLUTION_HT', '&#8212;');
define('CTX_NOT_CHECKED', '');
define('CTX_NOT_CHECKED_HT', ' ?');

$CTX_NAMES = array(
    "problems"=>array(
        "name"=>"Задача",
        "plural"=>"Задачи",
        "whom"=>"задачу",
    ),
    "submission"=>array(
        "name"=>"Присланное",
        "plural"=>"Присланное",
        "whom"=>"присланное",
    ),
);

global $XSM_ENUMS;

// Оценка решения
$XSM_ENUMS["resolution_mark"] = array(
    "values"=>array(
        CTX_NOT_CHECKED=>"Не проверена",
        CTX_NO_SOLUTION=>"Нет решения",
        CTX_STOLEN_SOLUTION=>"Списана",
        "0"=>"0",
        "1"=>"1",
        "2"=>"2",
        "3"=>"3",
        "4"=>"4",
        "5"=>"5",
        "6"=>"6",
        "7"=>"7",
        "8"=>"8",
        "9"=>"9",
        "10"=>"10",
    ),
    "default"=>CTX_NOT_CHECKED,
);

$CTX_META["problems"] = array(
    "problems_id" => array("name"=>"ID", "type"=>"pk"),
    "problem_name" => array("name"=>"Название задачи", "type"=>"text"),
    "people" => array("name"=>"Проверяющие", "type"=>"text"),
    "problem_html" => array("name"=>"Текст задачи", "type"=>"large"),
    "criteria" => array("name"=>"Критерий", "type"=>"large"),
);

$CTX_META["submission"] = array(
    "submission_id" => array("name"=>"ID", "type"=>"pk"),
    "mail" => array("name"=>"EMail", "type"=>"text"),
    "fileexchange" => array(
        "name"=>"Ссылка на файлообменник",
        "type"=>"link",
    ),
    "attachment" => array(
        "name"=>"Вложение",
        "type"=>"file",
    ),
    "submission_timestamp" => array(
        "name"=>"Время получения",
        "type"=>"timestamp",
        "readonly"=>true,
    ),
    "sender" => array(
        "name"=>"Отправитель",
        "type"=>"text",
        "readonly"=>true,
    ),
    "replied" => array(
        "name"=>"Отвечено",
        "type"=>"checkbox",
    ),
    "processed" => array(
        "name"=>"Обработано",
        "type"=>"checkbox",
    ),
);

$CTX_META["contestants"] = array(
    "contestants_id" => array("name"=>"", "type"=>"pk"),
    "name" => array(
        "name"=>"Ф.И.О. ученика",
        "type"=>"text",
        "required"=>true,
    ),
    "fileexchange" => array(
        "name"=>"Ссылка на файлообменник",
        "type"=>"link",
    ),
    "mail" => array("name"=>"Электропочта", "type"=>"text"),
    "phone" => array("name"=>"Телефон (и др. контакты)", "type"=>"text"),
    "parents" => array("name"=>"Родители", "type"=>"text"),
    "address" => array("name"=>"Адрес проживания", "type"=>"text"),
    "school" => array("name"=>"Школа", "type"=>"text"),
    "level" => array("name"=>"Класс", "type"=>"text"),
    "teacher_name" => array("name"=>"Преподаватель", "type"=>"text"),
    "work" => array("name"=>"Работа", "type"=>"file"),
    "status" => array("name"=>"Комментарии", "type"=>"large"),
);

$CTX_META["solutions"] = array(
    "solutions_id" => array("name"=>"pk", "type"=>"pk"),
    "problem_id" => array("name"=>"Идентификатор задачи", "type"=>"pk"),
    "contestant_id" => array("name"=>"Идентификатор работы", "type"=>"pk"),
    "resolution_text" => array("name"=>"Текст резолюции", "type"=>"large"),
    "resolution_author" => array("name"=>"Проверяющий", "type"=>"text"),
    "resolution_mark" => array("name"=>"Итоговая оценка", "type"=>"enum"),
);

function ctx_update_object($table_name, $new_values, $prev_values = array())
{
    global $CTX_META;
    global $CONTEST_CURRENT_YEAR;
    global $content_dir;

    $values = $prev_values;

    // directly update all non-file fields
    foreach ($CTX_META[$table_name] as $id=>$meta)
    {
        if ($meta["type"] == "file")
            continue;
        $values[$id] = xcms_get_key_or($new_values, $id);
    }

    // update file fields: if no new file given, preserve old value
    foreach ($CTX_META[$table_name] as $id=>$meta)
    {
        if ($meta["type"] != "file")
            continue;

        if (!@$_FILES[$id])
            continue;

        $file_desc = $_FILES[$id];

        if (!strlen($file_desc["tmp_name"]))
            continue;

        $timestamp = time();
        $home = "${content_dir}contest/attach/$table_name/$timestamp";
        $ext = pathinfo($file_desc["name"], PATHINFO_EXTENSION);
        $ext = xcms_to_valid_filename($ext);
        $file_name = pathinfo($file_desc["name"], PATHINFO_FILENAME);
        $file_name = xcms_to_valid_filename($file_name);
        if (xu_empty($file_name))
            $file_name = "file";
        $new_name = "$home/$table_name-attach-$file_name.$ext";
        @mkdir($home, 0777, true);
        file_put_contents("${content_dir}contest/attach/.htaccess", "Allow from all\n");
        if (!copy($file_desc["tmp_name"], $new_name))
            die("Cannot upload file. ");
        $values[$id] = $new_name;
    }

    $key_name = "${table_name}_id";
    $pk_value = xcms_get_key_or($values, $key_name, XDB_NEW);
    unset($values[$key_name]);
    $values["contest_year"] = $CONTEST_CURRENT_YEAR; // year sharding

    xdb_insert_or_update($table_name, array($key_name => $pk_value), $values, $values);
}

function ctx_get_works()
{
    global $FILTER;

    // store works by contestant_id
    $works_list = xdb_get_table("contestants", $FILTER);
    $works = array();
    foreach ($works_list as $work)
    {
        $id = $work["contestants_id"];
        $works[$id] = $work;
    }

    // join with solutions
    $sols = xdb_get_table("solutions", $FILTER);
    foreach ($sols as $sol)
    {
        $pid = $sol["problem_id"];
        $wid = $sol["contestant_id"];
        $works[$wid]["p$pid"] = $sol["resolution_mark"];
    }
    return $works;
}

function ctx_compare_undone_callback($a, $b)
{
    return strcmp($a["name"], $b["name"]);
}

function ctx_compare_done_callback($a, $b)
{
    if ($a["sum"] == $b["sum"])
        return strcmp($a["name"], $b["name"]);
    return $a["sum"] < $b["sum"];
}

function ctx_calculate_results(&$works, $probs)
{
    global $ref;

    $done = array();
    $undone = array();
    foreach ($works as &$work)
    {
        $id = @$work["contestants_id"];
        if (!$id)
            continue;

        $is_done = true;
        $sum = 0;
        foreach ($probs as $prob)
        {
            $pid = $prob["problems_id"];
            $val = @$work["p$pid"];
            if ($val === CTX_NOT_CHECKED)
            {
                $is_done = false;
            }
            $work["p${pid}val"] = $val;
            $sum += (integer)$val;
        }
        $work["sum"] = $sum;

        if ($is_done)
            $done[] = $work;
        else
            $undone[] = $work;
    }
    usort($done, 'ctx_compare_done_callback');
    usort($undone, 'ctx_compare_undone_callback');

    return array('done'=>$done, 'undone'=>$undone);
}
