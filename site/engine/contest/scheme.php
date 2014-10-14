<?php

$CONTEST_CURRENT_YEAR = "2014";

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
    "fileexchange" => array("name"=>"Ссылка на файлообменник", "type"=>"text"),
    "attachment" => array("name"=>"Вложение", "type"=>"file"),
    "submission_timestamp" => array("name"=>"Время получения", "type"=>"text", "readonly"=>true),
    "sender" => array("name"=>"Отправитель", "type"=>"text", "readonly"=>true),
);

$CTX_META["contestants"] = array(
    "contestants_id" => array("name"=>"", "type"=>"pk"),
    "name" => array(
        "name"=>"Ф.И.О. ученика",
        "type"=>"text",
        "required"=>true,
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
    "problem_id" => array("name"=>"Идентификатор проблемы", "type"=>"pk"),
    "contestant_id" => array("name"=>"Идентификатор работы", "type"=>"pk"),
    "resolution_text" => array("name"=>"Текст резолюции", "type"=>"large"),
    "resolution_author" => array("name"=>"Проверяющий", "type"=>"text"),
    "resolution_mark" => array("name"=>"Итоговая оценка", "type"=>"text"),
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
        $ext = xcms_page_id_suffix($ext);
        $file_name = pathinfo($file_desc["name"], PATHINFO_FILENAME);
        $file_name = xcms_page_id_suffix($file_name);
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
    $works_list = xdb_get_table("contestants", NULL, $FILTER);
    $works = array();
    foreach ($works_list as $work)
    {
        $id = $work["contestants_id"];
        $works[$id] = $work;
    }

    // join with solutions
    $sols = xdb_get_table("solutions", NULL, $FILTER);
    foreach ($sols as $sol)
    {
        $pid = $sol["problem_id"];
        $wid = $sol["contestant_id"];
        $works[$wid]["p$pid"] = $sol["resolution_mark"];
    }
    return $works;
}

function ctx_calculate_results(&$works, $probs)
{
    global $ref;

    $done = array();
    $undone = array();
    $done_sum = array();
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
            if (!strlen($val))
            {
                $val = "?";
                $is_done = false;
            }
            $work["p${pid}val"] = $val;
            $sum += (integer)$val;
        }
        $work["sum"] = $sum;

        if ($is_done)
        {
            @$done[$sum][] = $work;
            $done_sum[$sum] = $sum;
        }
        else $undone[] = $work;
    }
    rsort($done_sum);

    return array('done'=>$done, 'done_sum'=>$done_sum, 'undone'=>$undone);
}
