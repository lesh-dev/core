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
        return new SQlite3($db_name, SQLITE3_OPEN_READONLY);
    }

    function xmerger_open_db_write($db_name)
    {
        return new SQlite3($db_name, SQLITE3_OPEN_READWRITE);
    }

    function xmerger_get_selector($db, $table_name)
    {
        $query = "SELECT * FROM $table_name";
        return $db->query($query);
    }

    global $SETTINGS;
    // set db for writing
    $SETTINGS['xsm_db_name'] = "new.v2.sqlite3";

    $db_old = xmerger_open_db("old.v1.sqlite3");
    $db_cur = xmerger_open_db("current.v1.sqlite3");
    //$db_new = xmerger_open_db_write("new.v2.sqlite3");

    // person
    $person_sel = xmerger_get_selector($db_old, "person");
    while ($person_old = $person_sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_new = $person_old;
        // current_class -> ank_class
        $person_new['ank_class'] = $person_old['current_class'];
        unset($person_new['current_class']);
        // activity_status -> anketa_status
        $person_new['anketa_status'] = $person_old['activity_status'];
        unset($person_new['activity_status']);
        // comment: move to separate table
        $comment_text = $person_old['person_comment'];

        xdb_insert_ai("person", "person_id", array("person_id"=>$person_new["person_id"]), $person_new, false, false);
    }
?>
