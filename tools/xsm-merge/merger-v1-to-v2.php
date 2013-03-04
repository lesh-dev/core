<?php
    /**
      * Migration/merge script v1 to v2
      **/
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/unittest.php");
    require_once("${engine_dir}sys/auth.php");
    require_once("${engine_dir}sys/db.php");
    header("Content-Type: text/html; charset=utf-8");

    function xmerger_open_db($db_name)
    {
        xcms_log(XLOG_INFO, "Open database '$db_name'");
        return new SQlite3($db_name, SQLITE3_OPEN_READONLY);
    }

    function xmerger_open_db_write($db_name)
    {
        xcms_log(XLOG_INFO, "Open database '$db_name' for WRITING");
        return new SQlite3($db_name, SQLITE3_OPEN_READWRITE);
    }

    function xmerger_get_selector($db, $table_name)
    {
        $query = "SELECT * FROM $table_name";
        return $db->query($query);
    }

    function ctx_create_structure($path)
    {
        $db = xmerger_open_db_write("$path/new.v2.sqlite3");
        $db->exec("DROP TABLE IF EXISTS contestants;");
        $db->exec("CREATE TABLE contestants(contestants_id integer  PRIMARY KEY AUTOINCREMENT, name TEXT, mail TEXT, phone TEXT, parents TEXT, address TEXT, school TEXT, level TEXT, teacher_name TEXT, work TEXT, status TEXT);");
        $db->exec("DROP TABLE IF EXISTS problems;");
        $db->exec("CREATE TABLE problems(problems_id integer PRIMARY KEY AUTOINCREMENT , problem_name, problem_html, people text,criteria text);");
        $db->exec("DROP TABLE IF EXISTS solutions;");
        $db->exec("CREATE TABLE solutions(solutions_id integer PRIMARY KEY AUTOINCREMENT , problem_id, contestant_id integer, resolution_text, resolution_author, resolution_mark);");
        $db->exec("DROP TABLE IF EXISTS sol_discussion;");
        $db->exec("CREATE TABLE sol_discussion(sol_discussion_id integer PRIMARY KEY AUTOINCREMENT , problem_id,  contestant_id, author, comment);");
        $db->close();
    }

    function xmerger_copy_table($db_src, $table_name, $debug_type)
    {
        $obj_count = 0;
        xcms_log(XLOG_INFO, "Processing table '$table_name' [$debug_type]");
        $sel = xmerger_get_selector($db_src, $table_name);
        while ($obj = $sel->fetchArray(SQLITE3_ASSOC))
        {
            $key_name = "${table_name}_id";
            $id = $obj[$key_name];
            xcms_log(XLOG_DEBUG, "Read object '$table_name' #$id");

            $id_inserted = xdb_insert_ai($table_name, $key_name, $obj, $obj, XDB_NO_OVERRIDE_TS, XDB_NO_USE_AI);
            xcms_log(XLOG_DEBUG, "Write object '$table_name' #$id_inserted");
            $obj_count++;
        }
        return $obj_count;
    }

    global $SETTINGS;
    $path = ".";
    // set db for writing
    $SETTINGS['xsm_db_name'] = "$path/new.v2.sqlite3";

    $db_old = xmerger_open_db("$path/old.v1.sqlite3");
    $db_cur = xmerger_open_db("$path/current.v1.sqlite3");
    $db_new = xmerger_open_db_write("$path/new.v2.sqlite3");

    xcms_log(XLOG_INFO, "Clearing tables");
    // clear tables...
    $db_new->query("DELETE FROM person");
    $db_new->query("DELETE FROM person_comment");
    $db_new->query("DELETE FROM person_school");
    $db_new->query("DELETE FROM course");
    $db_new->query("DELETE FROM exam");
    $db_new->query("DELETE FROM school");
    $db_new->query("INSERT INTO school VALUES(1, 'ЛЭШ-2012', 'summmer', '2012.07.23', '2012.08.23', null, null)");
    $db_new->query("INSERT INTO school VALUES(2, 'ЗЭШ-2013', 'winter',  '2013.01.02', '2013.01.09', null, null)");
    $db_new->query("INSERT INTO school VALUES(3, 'ЛЭШ-2013', 'summer',  '2013.07.23', '2013.08.23', null, null)");
    $db_new->close();

    ctx_create_structure($path);

    $persons = 0;
    $person_comments = 0;
    $courses = 0;
    $exams = 0;
    $person_schools = 0;

    // first of all, incorporate all existing data from current database

    // person
    xcms_log(XLOG_INFO, "Processing current persons");
    $sel = xmerger_get_selector($db_cur, "person");
    while ($person_old = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_new = $person_old;
        $person_id = $person_old['person_id'];
        xcms_log(XLOG_DEBUG, "Read person $person_id");

        // apply name fixups
        $last_name = $person_old['last_name'];
        $first_name = $person_old['first_name'];
        if ($last_name == 'Афонина')
            $person_new['first_name'] = 'Маришка'; // like in old database
        if ($last_name == 'Коноваленко')
            $person_new['first_name'] = 'Даниил'; // like in old database
        if ($last_name == 'Додонова')
            $person_new['first_name'] = 'Алена'; // like in old database

        // copy current_class -> ank_class
        $person_new['ank_class'] = $person_old['current_class'];

        // activity_status -> anketa_status
        $person_new['anketa_status'] = $person_old['activity_status'];
        unset($person_new['activity_status']);

        // curatorship is absent in new person
        unset($person_new['curatorship']);

        // is_current is absent in new person
        unset($person_new['is_current']);

        // comment: move to separate table
        $comment_text = trim($person_old['person_comment']);
        unset($person_new['person_comment']);

        $person_id_inserted = xdb_insert_ai("person", "person_id", $person_new, $person_new, XDB_NO_OVERRIDE_TS, XDB_NO_USE_AI);
        xcms_log(XLOG_DEBUG, "Write person $person_id_inserted");
        $persons++;

        if (strlen($comment_text) > 0)
        {
            $person_comment = array(
                "comment_text"=>$comment_text,
                "blamed_person_id"=>$person_id,
                "owner_login"=>"anonymous",
                "person_comment_created"=>$person_new["person_created"],
                "person_comment_modified"=>$person_new["person_modified"],
                "person_comment_deleted"=>"");

            $person_comment_id = xdb_insert_ai("person_comment", "person_comment_id", $person_comment, $person_comment);
            xcms_log(XLOG_DEBUG, "Write person_comment $person_comment_id");
            $person_comments++;
        }

        if ($person_old['is_current'] == 'current')
        {
            $person_school = array(
                "member_person_id"=>$person_id,
                "school_id"=>"1",
                "is_student"=>$person_old["is_student"],
                "is_teacher"=>$person_old["is_teacher"],
                "curatorship"=>"",
                "current_class"=>$person_old["current_class"],
                "courses_needed"=>"8",
                "person_school_created"=>$person_new["person_created"],
                "person_school_modified"=>$person_new["person_modified"]);
            $person_school_id = xdb_insert_ai("person_school", "person_school_id", $person_school, $person_school);
            xcms_log(XLOG_DEBUG, "Write person_school $person_school_id");
            $person_schools++;
        }

    }

    // course
    xcms_log(XLOG_INFO, "Processing current courses");
    $sel = xmerger_get_selector($db_cur, "course");
    while ($course = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $course_id = $course['course_id'];
        xcms_log(XLOG_DEBUG, "Read course $course_id");

        $course['school_id'] = '1'; // lesh-2012=1, zesh-2013=2,

        $course_id_inserted = xdb_insert_ai("course", "course_id", $course, $course, XDB_NO_OVERRIDE_TS, XDB_NO_USE_AI);
        xcms_log(XLOG_DEBUG, "Write course $course_id_inserted");
        $courses++;
    }

    // exam
    $exams = xmerger_copy_table($db_cur, "exam", "current");
    // merge contest tables AS IS
    xmerger_copy_table($db_cur, "contestants", "current");
    xmerger_copy_table($db_cur, "problems", "current");
    xmerger_copy_table($db_cur, "solutions", "current");
    xmerger_copy_table($db_cur, "sol_discussion", "current");

    $merges = 0;
    // persons from old database
    xcms_log(XLOG_INFO, "Processing old persons");
    $sel = xmerger_get_selector($db_old, "person");
    while ($person_old = $sel->fetchArray(SQLITE3_ASSOC))
    {
        // fix upyachka with quotes in old records
        foreach ($person_old as $key => $value)
            $person_old[$key] = str_replace('\"', '"', $value);
        $person_new = $person_old;

        $person_id = $person_old['person_id'];
        xcms_log(XLOG_DEBUG, "Read person $person_id");
        $last_name = $person_old['last_name'];
        $first_name = $person_old['first_name'];

        // copy current_class -> ank_class
        $person_new['ank_class'] = $person_old['current_class'];
        //unset($person_new['current_class']);

        // activity_status -> anketa_status
        $person_new['anketa_status'] = $person_old['activity_status'];
        $status = $person_new['anketa_status'];
        if ($status == "spam" || $status == "duplicate")
        {
            // filter some trash
            xcms_log(XLOG_INFO, "DUP: Skipped [$status] $last_name $first_name");
            continue;
        }
        unset($person_new['activity_status']);
        // TODO: convert 'new' statuses to 'archive' ?

        // curatorship is absent in new person
        unset($person_new['curatorship']);

        // is_current is absent in new person
        unset($person_new['is_current']);

        // comment: move to separate table
        $comment_text = trim($person_old['person_comment']);
        unset($person_new['person_comment']);

        $dup_merged = false;
        $merge_fail = false;
        // duplicates are taken from new db
        $duplicates = xdb_get_table('person', '', "last_name = '$last_name'");
        $dup_count = count($duplicates);

        xcms_log(XLOG_INFO, "DUP: -------------------------------------------------");
        // detect duplicates and merge
        foreach ($duplicates as $person_dup)
        {
            // person_dup was taken from new_db
            $person_merged = $person_dup; // just a copy to compare
            foreach ($person_dup as $key => $value)
            {
                if ($key == "person_created" ||
                    $key == "person_modified" ||
                    $key == "person_id" ||
                    $key == "last_name" ||
                    $key == "anketa_status")
                continue;

                $new_value = trim($person_new[$key]);
                $value = trim($value);
                if (strlen($value) && strlen($new_value) && $value != $new_value)
                {
                    xcms_log(XLOG_INFO, "DUP: key conflict: $key|$value|$new_value");
                    $merge_fail = true;
                    continue;
                }
                $person_merged[$key] = $new_value;
            }
            if ($merge_fail)
            {
                xcms_log(XLOG_INFO, "DUP: Unresolved duplicate (see above) found for $last_name $first_name @ ".$person_dup['anketa_status']);
                break;
            }

            //xcms_log(XLOG_DEBUG, "DUP:   Merge OK");
            xdb_update("person", array("person_id"=>$person_merged['person_id']), $person_merged, $person_merged, XDB_NO_OVERRIDE_TS);
            //xcms_log(XLOG_DEBUG, "Update person ".$person_merged['person_id']);
            ++$merges;
            $dup_merged = true;
        }

        if (!$merge_fail && !$dup_merged)
        {
            // default status is old people
            $person_new['anketa_status'] = 'old';
            $person_id_inserted = xdb_insert_ai("person", "person_id", $person_new, $person_new, XDB_NO_OVERRIDE_TS);
            xcms_log(XLOG_DEBUG, "Write person $person_id_inserted");
            $persons++;
        }
        if ($merge_fail)
        {
            xcms_log(XLOG_INFO, "DUP:      count: $dup_count");
            $person_new['last_name'] .= ' NOT_MERGED';
            $person_new['anketa_status'] = 'new';
            $person_id_inserted = xdb_insert_ai("person", "person_id", $person_new, $person_new, XDB_NO_OVERRIDE_TS);
            xcms_log(XLOG_DEBUG, "Write person $person_id_inserted");
            $persons++;
        }

        if (strlen($comment_text) > 0)
        {
            $person_comment = array(
                "comment_text"=>$comment_text,
                "blamed_person_id"=>$person_id_inserted,
                "owner_login"=>"anonymous",
                "person_comment_created"=>$person_new["person_created"],
                "person_comment_modified"=>$person_new["person_modified"],
                "person_comment_deleted"=>"");

            $person_comment_id = xdb_insert_ai("person_comment", "person_comment_id", $person_comment, $person_comment);
            xcms_log(XLOG_DEBUG, "Write person_comment $person_comment_id");
            $person_comments++;
        }
    }

    xcms_log(XLOG_INFO, "========================================================");
    xcms_log(XLOG_INFO, "Persons processed: $persons");
    xcms_log(XLOG_INFO, "Person merges: $merges");
    xcms_log(XLOG_INFO, "Person comments processed: $person_comments");
    xcms_log(XLOG_INFO, "Person schools processed: $person_schools");
    xcms_log(XLOG_INFO, "Courses processed: $courses");
    xcms_log(XLOG_INFO, "Exams processed: $exams");
    xcms_log(XLOG_INFO, "Merged contestants, solutions, problems, sol_discussion tables");
?>
