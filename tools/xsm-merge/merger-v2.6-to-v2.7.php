<?php
    /**
      * Migration/merge script v2.6 to v2.7
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
    $SETTINGS['xsm_db_name'] = "$path/fizlesh.sqlite3";
    $db = xdb_open_db_write("$path/fizlesh.sqlite3");
    $courses = 0;

    // Create department table
    $db->exec(
        "CREATE TABLE department (
        department_id integer primary key autoincrement,
        department_title text,
        department_created text, -- utc timestamp
        department_modified text -- utc timestamp
        );");

    // Create departments
    $db->exec("INSERT INTO department (department_title, department_created) VALUES ('Физическое', '2005.08.23 01:02:03');");
    $db->exec("INSERT INTO department (department_title, department_created) VALUES ('Другое', '1990.01.01 01:02:03');");

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

        lesh_ref text,       -- откуда узнали о школе (2.1+)

        forest_1 text,       -- 1-й выход в лес (2.3a+)
        forest_2 text,       -- 2-й выход в лес (2.3a+)
        forest_3 text,       -- 3-й выход в лес (2.3a+)

        tent_capacity text,   -- количество мест в палатке (0 = палатки нет) (2.2+)
        tour_requisites text, -- имеющиеся предметы туристского обихода (2.2+)

        anketa_status text, -- former activity_status
            -- enum:(new, processed, declined, taken, duplicated, spam)

        user_agent text,    -- идентификатор браузера, с которого была подана анкета

        department_id integer not null, -- ссылка на отделение

        person_created text, -- utc timestamp
        person_modified text, -- utc timestamp

        foreign key (department_id) references department(department_id)
    );");

    // person: add department_id fk
    xcms_log(XLOG_INFO, "Processing persons");
    $sel = xdb_get_selector($db, "person");
    $persons = 0;
    while ($person = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_id = $person["person_id"];
        $person["department_id"] = 1;
        xdb_insert_ai("person_new", "person_id", $person, $person, XDB_OVERRIDE_TS, XDB_NO_USE_AI, $db);
        ++$persons;
    }

    // rename table
    $db->exec("DROP TABLE person");

    $db->exec("ALTER TABLE person_new RENAME TO person");
    xcms_log(XLOG_INFO, "persons processed: $persons");

    // person_school: add department_id fk
    $db->exec(
        "CREATE TABLE person_school_new (
        person_school_id integer primary key autoincrement,
        member_person_id integer not null, -- fk person
        member_department_id integer not null, -- fk department
        school_id integer not null, -- fk school
        is_student text, -- является ли школьником на данной школе
        is_teacher text, -- является ли преподом на данной школе
        curatorship text, -- кураторство на данной школе enum:(никто, помкур, куратор)
        current_class text, -- класс, в котором находится школьник
            -- (для Летней школы надо договориться, какой именно класс мы ставим,
            -- будущий или прошедший
        courses_needed integer, -- потребное кол-во курсов для сдачи на школе
        person_school_created text, -- utc timestamp
        person_school_modified text, -- utc timestamp
        foreign key (member_person_id) references person(person_id),
        foreign key (member_department_id) references department(department_id),
        foreign key (school_id) references school(school_id)
        );");


    $sel = xdb_get_selector($db, "person_school");
    $person_schools = 0;
    while ($person_school = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_school_id = $person["person_school_id"];
        $person_school["member_department_id"] = 1;
        xdb_insert_ai("person_school_new", "person_school_id", $person_school, $person_school, XDB_OVERRIDE_TS, XDB_NO_USE_AI, $db);
        ++$person_schools;
    }

    // rename table
    $db->exec("DROP TABLE person_school");

    $db->exec("ALTER TABLE person_school_new RENAME TO person_school");
    xcms_log(XLOG_INFO, "person_schools processed: $person_schools");

    $db->exec("ALTER TABLE `school` ADD COLUMN `school_location` text;");

    xdb_vacuum();
?>
