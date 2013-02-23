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

    function msg($m)
    {
        echo "$m\n";
    }

    global $SETTINGS;
    // set db for writing
    $SETTINGS['xsm_db_name'] = "new.v2.sqlite3";

    $db_old = xmerger_open_db("old.v1.sqlite3");
    $db_cur = xmerger_open_db("current.v1.sqlite3");
    $db_new = xmerger_open_db_write("new.v2.sqlite3");

    msg("Clearing tables");
    // clear tables...
    $db_new->query("DELETE FROM person");
    $db_new->query("DELETE FROM person_comment");
    $db_new->close();

    // person
    $person_sel = xmerger_get_selector($db_old, "person");
    msg("Processing persons");
    while ($person_old = $person_sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_new = $person_old;
        $person_id = $person_old['person_id'];
        msg("  Read person $person_id");

        // current_class -> ank_class
        $person_new['ank_class'] = $person_old['current_class'];
        unset($person_new['current_class']);
        // activity_status -> anketa_status
        $person_new['anketa_status'] = $person_old['activity_status'];
        unset($person_new['activity_status']);

        // curatorship is absent in new person
        unset($person_new['curatorship']);

        // TODO: is_current -> person_school for LESH-2012
        unset($person_new['is_current']);

        // comment: move to separate table
        $comment_text = trim($person_old['person_comment']);
        unset($person_new['person_comment']);

        $person_id_inserted = xdb_insert_ai("person", "person_id", $person_new, $person_new, false, false);
        msg("  Write person $person_id_inserted");

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
            msg("  Write person_comment $person_comment_id");
        }
    }
?>
