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
    $path = ".";
    // set db for writing
    $SETTINGS['xsm_db_name'] = "$path/fizlesh.sqlite3";
    $SETTINGS['xsm_need_open_db'] = "$path/fizlesh.sqlite3";
    $db = xmerger_open_db_write("$path/fizlesh.sqlite3");
    $courses = 0;

    // first of all, incorporate all existing data from current database
    $db->exec(
        "CREATE TABLE person_new (
        person_id integer primary key autoincrement,

        last_name text, -- фамилия
        first_name text, -- имя
        patronymic text, -- отчество

        birth_date text, -- дата рождения
        passport_data text, -- паспортные данные

        school text,        -- школа, в которой учится школьник
        school_city text,   -- город, в котором находится школа
        ank_class text,     -- класс подачи заявки
        current_class text, -- текущий класс

        phone text,         -- телефон (городской)
        cellular text,      -- мобильный телефон
        email text,         -- контактный email
        skype text,         -- skype
        social_profile text,  -- профиль ВКонтакте и т.п. (используемый!)

        is_teacher text, -- типично препод
        is_student text, -- типично школьник

        favourites text,     -- любимые предметы
        achievements text,   -- достижения
        hobby text,          -- хобби

        tent_capacity text,   -- количество мест в палатке (0 = палатки нет)
        tour_requisites text, -- имеющиеся предметы туристского обихода

        anketa_status text, -- former activity_status
            -- enum:(new, processed, declined, taken, duplicated, spam)

        user_agent text,    -- идентификатор браузера, с которого была подана анкета

        department_id integer not null, -- ссылка на отделение

        person_created text, -- utc timestamp
        person_modified text, -- utc timestamp

        foreign key (department_id) references department(department_id)"
    );

    // course: move teacher info into separate course_teacher table
    xcms_log(XLOG_INFO, "Processing persons");
    $sel = xmerger_get_selector($db, "person");
    $persons = 0;
    while ($person = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_id = $person["person_id"];
        $person["department_id"] = 1;
        xdb_insert_ai("person_new", "person_id", $person, $person, XDB_OVERRIDE_TS, XDB_USE_AI, $db);
        ++$persons;
    }

    // rename table
    $db->exec("DROP TABLE person");

    $db->exec("ALTER TABLE person_new RENAME TO person");
    xcms_log(XLOG_INFO, "persons processed: $persons");

    $db->exec("VACUUM");
    xcms_log(XLOG_INFO, "Database vacuumed");
?>
