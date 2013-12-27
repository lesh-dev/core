<?php

function ctx_create_structure()
{
    $db = xdb_get_write();
    $db->exec("DROP TABLE contestants;");
    $db->exec("CREATE TABLE contestants(
        contestants_id integer PRIMARY KEY AUTOINCREMENT,
        name text,
        mail text,
        phone text,
        parents text,
        address text,
        school text,
        level text,
        teacher_name text,
        work text,
        status text,
        contest_year text
        );");

    $db->exec("DROP TABLE problems;");
    $db->exec("CREATE TABLE problems(
        problems_id integer PRIMARY KEY AUTOINCREMENT,
        problem_name text,
        problem_html text,
        people text,
        criteria text,
        contest_year text
        );");

    $db->exec("DROP TABLE solutions;");
    $db->exec("CREATE TABLE solutions(
        solutions_id integer PRIMARY KEY AUTOINCREMENT,
        problem_id,
        contestant_id integer,
        resolution_text text,
        resolution_author text,
        resolution_mark text,
        contest_year text
        );");

    /*
    $db->exec("DROP TABLE sol_discussion;");
    $db->exec("CREATE TABLE sol_discussion(
        sol_discussion_id integer PRIMARY KEY AUTOINCREMENT,
        problem_id,
        contestant_id,
        author text,
        comment text,
        contest_year text
        );");*/
}

function ctx_update_object($table_name, $values)
{
    global $CTX_META;
    global $CONTEST_CURRENT_YEAR;
    global $content_dir;

    foreach($CTX_META[$table_name] as $id=>$arr)
    {
        $values[$id] = @$_POST[$id];
        if (!@$_FILES[$id])
            continue;

        if (empty($_FILES[$id]["tmp_name"]))
            continue;

        $home = "$content_dir/contest/attach/$table_name/".time();
        $new_name = "$home/".$_FILES[$id]["name"];
        @mkdir("$home", 0777, true);
        if (!copy($_FILES[$id]["tmp_name"], $new_name))
            die("Cannot upload file. ");
        $values[$id] = $new_name;
    }

    $key_name = "${table_name}_id";
    $pkv = $values[$key_name];
    unset($values[$key_name]);
    $values["contest_year"] = $CONTEST_CURRENT_YEAR; // year sharding
    xdb_insert_or_update($table_name, array($key_name => $pkv), $values, $values);
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
            if (!$val)
            {
                $val = "?";
                $is_done = false;
            }
            $work["p${pid}val"] = $val;
            $sum += (integer)$val;
        }
        if ($is_done)
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

function ctx_print_result_row($work, $probs)
{
    global $ref;
    $id = $work["contestants_id"];
    $row =
        "<td><a ".xcms_href(array(
            'ref'=>$ref, 'mode'=>'view', 'table'=>'contestants', 'id'=>$id)).">{$work['name']}</a></td>".
        "<td>{$work['level']}</td>".
        "<td><a href=\"{$work['work']}\">Скачать</a></td>";

    foreach ($probs as $prob)
    {
        $pid = $prob["problems_id"];
        $row .= "<td>";
        $mark = $work["p${pid}val"];
        $row .= $mark;
        $row .= "</td>";
    }
    $sum = @$work['sum'];
    if ($sum)
        $row .= "<td>$sum</td>";

    $row .= "<td><a ".xcms_href(array(
        'ref'=>$ref, 'mode'=>'delete', 'table'=>'contestants', 'id'=>$id)).">Удалить</a></td>";

    return $row;
}
