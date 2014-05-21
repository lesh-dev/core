<?php
    /**
      * Migration/merge script v2.3 to v2.4
      **/
    date_default_timezone_set('Europe/Moscow');
    require_once("settings.php");
    require_once("${engine_dir}sys/settings.php");
    require_once("${engine_dir}sys/unittest.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/util.php");
    require_once("${engine_dir}sys/auth.php");
    require_once("${engine_dir}sys/db.php");
    header("Content-Type: text/html; charset=utf-8");

    global $SETTINGS;
    $path = ".";
    $db_path = "$path/fizlesh.sqlite3";
    // set db for writing
    $SETTINGS['xsm_db_name'] = $db_path;
    $db = xmerger_open_db_write($db_path);
    $courses = 0;

    // first of all, incorporate all existing data from current database

    $db->exec("CREATE TABLE course_new (".
        "course_id integer primary key autoincrement, ".
        "course_title text, ".
        "school_id integer not null, ".
        "course_cycle text, ".
        "target_class text, ".
        "course_desc text, ".
        "course_comment text, ".
        "course_created text, ".
        "course_modified text ".
        ");");

    $db->exec("CREATE TABLE course_teachers (".
        "course_teachers_id integer primary key autoincrement, ".
        "course_id integer not null, ".
        "course_teacher_id integer not null, ".
        "course_teachers_created text, ".
        "course_teachers_modified text, ".
        "foreign key (course_id) references course(course_id), ".
        "foreign key (course_teacher_id) references person(person_id) ".
        ");");

    // course: move teacher info into separate course_teacher table
    xcms_log(XLOG_INFO, "Processing courses");
    $sel = xdb_get_selector($db, "course");
    while ($course = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $course_id = $course["course_id"];
        $course_teacher_id = $course["course_teacher_id"];
        $course_teacher = array(
            "course_id"=>$course_id,
            "course_teacher_id"=>$course_teacher_id
        );
        xdb_insert_ai("course_teachers", "course_teachers_id", $course_teacher, $course_teacher, XDB_OVERRIDE_TS, XDB_USE_AI, $db);
    }

    // course: drop course_teacher_id column
    xcms_log(XLOG_INFO, "Drop course_teacher_id column");
    $sel = xdb_get_selector($db, "course");
    while ($course = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $course_id = $course['course_id'];
        xcms_log(XLOG_DEBUG, "Read course $course_id");
        unset($course["course_teacher_id"]);

        $course_id_inserted = xdb_insert_ai("course_new", "course_id", $course, $course, XDB_NO_OVERRIDE_TS, XDB_NO_USE_AI, $db);
        xcms_log(XLOG_DEBUG, "Write course $course_id_inserted");
        $courses++;
    }

    // rename table
    $db->exec("DROP TABLE course");

    $db->exec("ALTER TABLE course_new RENAME TO course");
    xcms_log(XLOG_INFO, "Courses processed: $courses");

    $db->exec("VACUUM");
    xcms_log(XLOG_INFO, "Database vacuumed");
?>
