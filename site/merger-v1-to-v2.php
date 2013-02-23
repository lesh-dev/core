<?php
    /*
    Migration/merge script v1 to v2
    */
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

    global $SETTINGS;
    $path = "./engine/dbpatches/2013.03.03-v1-to-v2";
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
    $db_new->close();

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

        // current_class -> ank_class
        $person_new['ank_class'] = $person_old['current_class'];
        unset($person_new['current_class']);
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

        $person_id_inserted = xdb_insert_ai("person", "person_id", $person_new, $person_new, false, false);
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

        $course_id_inserted = xdb_insert_ai("course", "course_id", $course, $course, false, false);
        xcms_log(XLOG_DEBUG, "Write course $course_id_inserted");
        $courses++;
    }

    // exam
    xcms_log(XLOG_INFO, "Processing current exams");
    $sel = xmerger_get_selector($db_cur, "exam");
    while ($exam = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $exam_id = $exam['exam_id'];
        xcms_log(XLOG_DEBUG, "Read exam $exam_id");

        $exam_id_inserted = xdb_insert_ai("exam", "exam_id", $exam, $exam, false, false);
        xcms_log(XLOG_DEBUG, "Write exam $exam_id_inserted");
        $exams++;
    }
    // TODO: contestants, problems, solutions !!!

    xcms_log(XLOG_INFO, "========================================================");
    xcms_log(XLOG_INFO, "Persons processed: $persons");
    xcms_log(XLOG_INFO, "Person comments processed: $person_comments");
    xcms_log(XLOG_INFO, "Person schools processed: $person_schools");
    xcms_log(XLOG_INFO, "Courses processed: $courses");
    xcms_log(XLOG_INFO, "Exams processed: $exams");
    xcms_log(XLOG_INFO, "Contestants processed: NONE");

?>
