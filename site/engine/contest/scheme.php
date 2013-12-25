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
