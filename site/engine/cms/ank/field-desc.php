<?php

define('XSM_SCHOOL_ANK_ID', 'ank');

// Person
function xsm_get_person_fields()
{
    return array(
        "department_id"=>"Отделение",

        "anketa_status"=>"Статус",

        "last_name"=>"Фамилия",
        "first_name"=>"Имя",
        "patronymic"=>"Отчество",

        "birth_date"=>"Дата рождения",
        "passport_data"=>"Паспортные данные",

        "school"=>"Школа",
        "school_city"=>"Адрес школы",
        "ank_class"=>"Класс подачи анкеты",
        "current_class"=>"Класс",

        "phone"=>"Телефон",
        "cellular"=>"Мобильный телефон",
        "email"=>"E-Mail",
        "skype"=>"Skype",
        "social_profile"=>"Профиль в соц. сети",

        "is_teacher"=>"Препод",
        "is_student"=>"Школьник",

        "tent_capacity"=>"Вместимость палатки",
        "tour_requisites"=>"Туристское барахло",

        "forest_1"=>"1-й выход в лес",
        "forest_2"=>"2-й выход в лес",
        "forest_3"=>"3-й выход в лес",

        "favourites"=>"Любимые предметы",
        "achievements"=>"Достижения",
        "hobby"=>"Хобби",
        "lesh_ref"=>"Откуда узнали о школе",

        "user_agent"=>"UserAgent",

        "person_created"=>"Время создания",
        "person_modified"=>"Последняя модификация"
    );
}

function xsm_get_person_field_types()
{
    return array(
        "favourites"=>"textarea",
        "achievements"=>"textarea",
        "hobby"=>"textarea",
        "lesh_ref"=>"textarea",
        "tour_requisites"=>"textarea",

        "is_teacher"=>"checkbox",
        "is_student"=>"checkbox",

        "anketa_status"=>"enum",

        "forest_1"=>"enum",
        "forest_2"=>"enum",
        "forest_3"=>"enum"
    );
}

// Person on School
function xsm_get_person_school_fields()
{
    return array(
        "member_person_id"=>"Участник",
        "school_id"=>"Школа",
        "member_department_id"=>"Отделение",
        "is_student"=>"Школьник",
        "current_class"=>"Класс",
        "courses_needed"=>"Потребное кол-во зачётов",
        "curator_group"=>"Кто курирует",
        "is_teacher"=>"Препод",
        "curatorship"=>"Кураторство",
        "person_school_created"=>"Время создания",
        "person_school_modified"=>"Последняя модификация"
    );
}

// Person comment
function xsm_get_person_comment_fields()
{
    return array(
        "comment_text"=>"Текст комментария",
        "owner_login"=>"Логин автора",
        "blamed_person_id"=>"ID субъекта",
        "person_comment_created"=>"Время создания",
        "person_comment_modified"=>"Последняя модификация",
        "person_comment_deleted"=>"Объект удалён"
    );
}

function xsm_get_person_comment_field_types()
{
    return array(
        "comment_text"=>"textarea",
    );
}

function xsm_get_person_comment_field_req()
{
    return array(
        "comment_text"=>"required",
    );
}

// new style field descriptors
function xsm_get_fields($table_name)
{
    $field_desc = array(

        // department
        "department"=>array(
            "department_title"=>array(
                "name"=>"Название",
                "required"=>true,
            ),
            "department_created"=>array(
                "name"=>"Время создания",
            ),
            "department_modified"=>array(
                "name"=>"Последняя модификация",
            ),
        ),

        // school
        "school"=>array(
            "school_title"=>array(
                "name"=>"Название",
                "required"=>true,
            ),
            "school_type"=>array(
                "name"=>"Тип",
                "type"=>"enum",
            ),
            "school_date_start"=>array(
                "name"=>"Дата начала (ГГГГ.ММ.ДД)",
            ),
            "school_date_end"=>array(
                "name"=>"Дата окончания (ГГГГ.ММ.ДД)",
            ),
            "school_location"=>array(
                "name"=>"Место проведения",
            ),
            "school_created"=>array(
                "name"=>"Время создания",
            ),
            "school_modified"=>array(
                "name"=>"Последняя модификация",
            ),
        ),

        "person"=>array(
            "department_id"=>array(
                "name"=>"Отделение",
            ),

            "anketa_status"=>array(
                "name"=>"Статус",
                "type"=>"enum",
            ),

            "last_name"=>array(
                "name"=>"Фамилия",
            ),
            "first_name"=>array(
                "name"=>"Имя",
            ),
            "patronymic"=>array(
                "name"=>"Отчество",
            ),

            "birth_date"=>array(
                "name"=>"Дата рождения",
            ),
            "passport_data"=>array(
                "name"=>"Паспортные данные",
            ),

            "school"=>array(
                "name"=>"Школа",
            ),
            "school_city"=>array(
                "name"=>"Адрес школы",
            ),
            "ank_class"=>array(
                "name"=>"Класс подачи анкеты",
            ),
            "current_class"=>array(
                "name"=>"Класс",
            ),

            "phone"=>array(
                "name"=>"Телефон",
            ),
            "cellular"=>array(
                "name"=>"Мобильный телефон",
            ),
            "email"=>array(
                "name"=>"E-Mail",
            ),
            "skype"=>array(
                "name"=>"Skype",
            ),
            "social_profile"=>array(
                "name"=>"Профиль в соц. сети",
            ),

            "is_teacher"=>array(
                "name"=>"Препод",
                "type"=>"checkbox",
            ),
            "is_student"=>array(
                "name"=>"Школьник",
                "type"=>"checkbox",
            ),

            "tent_capacity"=>array(
                "name"=>"Вместимость палатки",
            ),
            "tour_requisites"=>array(
                "name"=>"Туристское барахло",
                "type"=>"textarea",
            ),

            "forest_1"=>array(
                "name"=>"1-й выход в лес",
                "type"=>"enum",
            ),
            "forest_2"=>array(
                "name"=>"2-й выход в лес",
                "type"=>"enum",
            ),
            "forest_3"=>array(
                "name"=>"3-й выход в лес",
                "type"=>"enum",
            ),

            "favourites"=>array(
                "name"=>"Любимые предметы",
                "type"=>"textarea",
            ),
            "achievements"=>array(
                "name"=>"Достижения",
                "type"=>"textarea",
            ),
            "hobby"=>array(
                "name"=>"Хобби",
                "type"=>"textarea",
            ),
            "lesh_ref"=>array(
                "name"=>"Откуда узнали о школе",
                "type"=>"textarea",
            ),

            "user_agent"=>array(
                "name"=>"UserAgent",
                "readonly"=>true,
            ),

            "person_created"=>array(
                "name"=>"Время создания",
            ),
            "person_modified"=>array(
                "name"=>"Последняя модификация",
            ),
        ),

        // person_comment
        "person_comment"=>array(
            "comment_text"=>array(
                "name"=>"Текст комментария",
                "type"=>"textarea",
                "required"=>true,
            ),
            "owner_login"=>array(
                "name"=>"Логин автора",
                "readonly"=>true,
            ),
            "blamed_person_id"=>array(
                "name"=>"ID субъекта",
                "readonly"=>true,
            ),
            "person_comment_created"=>array(
                "name"=>"Время создания",
            ),
            "person_comment_modified"=>array(
                "name"=>"Последняя модификация",
            ),
            "person_comment_deleted"=>array(
                "name"=>"Объект удалён",
            ),
        ),

        // exam
        "exam"=>array(
            "student_person_id"=>array(
                "name"=>"Школьник",
            ),
            "course_id"=>array(
                "name"=>"Курс",
            ),
            "exam_status"=>array(
                "name"=>"Состояние",
                "type"=>"enum",
            ),
            "deadline_date"=>array(
                "name"=>"Дедлайн",
            ),
            "exam_comment"=>array(
                "name"=>"Комментарий к зачёту",
                "type"=>"textarea",
            ),
            "exam_created"=>array(
                "name"=>"Время создания",
            ),
            "exam_modified"=>array(
                "name"=>"Последняя модификация",
            ),
        ),

    );
    return $field_desc[$table_name];
}

// Course
function xsm_get_course_fields()
{
    return array(
        "course_title"=>"Название курса",
        "target_class"=>"Уровень (диапазон классов)",
        "school_id"=>"Школа, на которой читался курс",
        "course_cycle"=>"Цикл, на котором читался курс",
        "course_desc"=>"Описание",
        "course_type"=>"Тип курса",
        "course_area"=>"Тематика",
        "course_comment"=>"Комментарий",
        "course_created"=>"Время создания",
        "course_modified"=>"Последняя модификация"
    );
}

function xsm_get_course_field_types()
{
    return array(
        "course_comment"=>"textarea",
        "course_desc"=>"textarea",
        "course_type"=>"enum",
        "course_area"=>"enum"
    );
}

function xsm_get_course_teachers_fields()
{
    return array(
        "course_id"=>"Курс",
        "course_teacher_id"=>"Препод курса",
        "course_teachers_created"=>"Время создания",
        "course_teachers_modified"=>"Последняя модификация"
    );
}

// Exam
function xsm_get_exam_fields()
{
    return array(
        "student_person_id"=>"Школьник",
        "course_id"=>"Курс",
        "exam_status"=>"Состояние",
        "deadline_date"=>"Дедлайн",
        "exam_comment"=>"Комментарий к зачёту",
        "exam_created"=>"Время создания",
        "exam_modified"=>"Последняя модификация"
    );
}

function xsm_get_exam_field_types()
{
    return array(
        "exam_comment"=>"textarea",
        "exam_status"=>"enum",
    );
}


$XSM_ENUMS = array(
    // статус анкеты (значения в базе)
    "anketa_status"=>array(
        "values"=>array(
            "new"=>"Новый",
            "progress"=>"Ждёт собес.",
            "less"=>"Ждёт леса",
            "processed"=>"Принят",
            "discuss"=>"Обсуждается",
            "nextyear"=>"Отложен",
            "declined"=>"Отклонён",
            "cont"=>"Активный",
            "old"=>"Архив",
            "duplicate"=>"Дубль",
            "spam"=>"Спам"),
        "default"=>"new"),

    // селектор для list-person-locator
    "show_anketa_status_locator"=>array(
        "values"=>array(
            "active"=>"Актив",
            "no-trash"=>"Все",
            "not-decl"=>"Все, кроме посланных",
            "not-old"=>"Все, кроме архивных",
            "processed"=>"Принятые",
            "cont"=>"Продолжающие",
            "old"=>"Архивные",
            "all"=>"Без фильтрации"),
        "default"=>"active"),

    // селектор для list-ank
    "show_anketa_status_ank"=>array(
        "values"=>array(
            "abitur"=>"Набор",
            "new"=>"Новые",
            "progress"=>"Ждут собеседования",
            "less"=>"Ждут леса",
            "processed"=>"Принятые",
            "nextyear"=>"Отложенные",
            "discuss"=>"Обсуждаются",
            "declined"=>"Отклонённые",
            "old"=>"Архивные",
            "no-trash"=>"Все",
            "all"=>"Без фильтрации"),
        "default"=>"abitur"),

    // Статус выхода в лес
    "forest_status"=>array(
        "values"=>array(
            "undef"=>"&mdash;",
            "notable"=>"Не может",
            "no"=>"Не идёт",
            "maybe"=>"ХЗ",
            "able"=>"Может",
            "yes"=>"Идёт"),
        "default"=>"undef"),

    // Фильтр для показов выходов в лес
    "show_forest_num"=>array(
        "values"=>array(
            "all"=>"Все выходы",
            "forest_1"=>"1-й выход",
            "forest_2"=>"2-й выход",
            "forest_3"=>"3-й выход"),
        "default"=>"all"),

    // Кураторство
    "curatorship"=>array(
        "values"=>array(
            "none"=>"Не куратор",
            "assist"=>"Помощник куратора",
            "cur"=>"Куратор"),
        "default"=>"none"),

    // Зачёт
    "exam_status"=>array(
        "values"=>array(
            "listen"=>"Прослушан",
            "passed"=>"Сдан",
            "notpassed"=>"Не сдан",
            "almost"=>"Почти сдан",
            "other"=>"Иное"),
        "default"=>"listen"),

    // Тип школы
    "school_type"=>array(
        "values"=>array(
            "lesh"=>"Летняя",
            "zesh"=>"Зимняя",
            "vesh"=>"Весеннняя"),
        "default"=>"lesh"),

    // Тип курса
    "course_type"=>array(
        "values"=>array(
            "generic"=>"Обычный",
            "facult"=>"Факультатив",
            "prac"=>"Практикум",
            "other"=>"Иное"),
        "default"=>"generic"),

    // Тематика курса
    "course_area"=>array(
        "values"=>array(
            "unknown"=>"Не выбрано",
            "precise"=>"Точные науки",
            "nature"=>"Естественные науки",
            "human"=>"Гуманитарные науки",
            "other"=>"Иное"),
        "default"=>"unknown")

);

// Enum API
function xsm_get_enum($enum_type)
{
    global $XSM_ENUMS;
    return $XSM_ENUMS[$enum_type]["values"];
}

function xsm_get_enum_default_value($enum_type)
{
    global $XSM_ENUMS;
    return $XSM_ENUMS[$enum_type]["default"];
}

function xsm_enum_exists($enum_type)
{
    global $XSM_ENUMS;
    return array_key_exists($enum_type, $XSM_ENUMS);
}

function xsm_check_enum_key($enum_type, $key)
{
    global $XSM_ENUMS;
    $enum_data = $XSM_ENUMS[$enum_type];
    if (!array_key_exists($key, $enum_data["values"]))
        return $enum_data["default"];
    return $key;
}

function xsm_get_persistent_enum_key($scope, $name, $enum_type)
{
    $default = xsm_get_enum_default_value($enum_type);
    $key = xcms_get_persistent_key($scope, $name, $default);
    return xsm_check_enum_key($enum_type, $key);
}


// Wrapper around generic API call
function xsm_make_enum_by_type($name, $value, $enum_type)
{
    return xsm_make_enum_selector($name, $value, xsm_get_enum($enum_type));
}

function xsm_saved_form($table_name)
{
    $forms = array(
        'school'=>'сохранена',
        'department'=>'сохранено',
        );
    return xcms_get_key_or($forms, $table_name, 'сохранён');
}

?>