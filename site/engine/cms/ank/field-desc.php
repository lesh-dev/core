<?php

define('XSM_SCHOOL_ANK_ID', 'ank');

// Department
function xsm_get_department_fields()
{
    return array(
        "department_title"=>"Название",
        "department_created"=>"Время создания",
        "department_modified"=>"Последняя модификация"
    );
}

// School (indeed, it can be all major events)
function xsm_get_school_fields()
{
    return array(
        "school_title"=>"Название",
        "school_type"=>"Тип",
        "school_date_start"=>"Дата начала (ГГГГ.ММ.ДД)",
        "school_date_end"=>"Дата окончания (ГГГГ.ММ.ДД)",
        "school_location"=>"Место проведения",
        "school_created"=>"Время создания",
        "school_modified"=>"Последняя модификация"
    );
}

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