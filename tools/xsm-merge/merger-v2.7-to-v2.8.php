<?php
    /**
      * Migration/merge script v2.7 to v2.8
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
    // set db for writing
    $db_path = "$path/fizlesh.sqlite3";
    $SETTINGS['xsm_db_name'] = $db_path;
    $db = xdb_open_db_write($db_path);
    $courses = 0;

    // Alter courses
    $db->exec("ALTER TABLE course ADD COLUMN course_type text");
    $db->exec("ALTER TABLE course ADD COLUMN course_area text");

    xdb_drop_column($db, "exam", "is_prac",
        "CREATE TABLE exam_new (
            exam_id integer primary key autoincrement, -- not used
            student_person_id integer not null, -- fk
            course_id integer not null, -- fk
            exam_status text,
            deadline_date text,
            exam_comment text,
            exam_created text,
            exam_modified text,
            foreign key (student_person_id) references person(person_id),
            foreign key (course_id) references course(course_id))");

    xdb_vacuum();
?>
