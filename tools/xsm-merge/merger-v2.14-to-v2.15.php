<?php
    /**
      * Migration/merge script v2.14 to v2.15
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
    $path = "/var/www/vhosts/fizlesh.ru/fizlesh.ru-content/ank";
    // set db for writing
    $db_path = "$path/fizlesh.sqlite3";
    $SETTINGS['xsm_db_name'] = $db_path;
    $db = xdb_open_db_write($db_path);

    $table_name = "person_comment";

    // create table with new structure
    $db->exec(
        "CREATE TABLE ${table_name}_new (
            person_comment_id integer primary key autoincrement,
            comment_text text,
            blamed_person_id integer not null,
            school_id integer,
            owner_login text not null,
            record_acl text,
            person_comment_created text,
            person_comment_modified text,
            person_comment_deleted text,
            person_comment_changedby text,
            foreign key (blamed_person_id) references person(person_id),
            foreign key (school_id) references school(school_id)
        )"
    );

    // copy data to new table
    $sel = xdb_get_selector($db, $table_name);
    $objects = 0;
    while ($obj = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $idn = "${table_name}_id";
        $object_id = $obj[$idn];
        $obj["record_acl"] = "ank";
        xdb_insert_ai("${table_name}_new", $idn, $obj, $obj, XDB_OVERRIDE_TS, XDB_NO_USE_AI, $db);
        ++$objects;
    }

    // rename table
    $db->exec("DROP TABLE $table_name");
    $db->exec("ALTER TABLE ${table_name}_new RENAME TO $table_name");
    xcms_log(XLOG_INFO, "[DB] Created new $table_name, processed $objects objects");

    xdb_vacuum($db);
