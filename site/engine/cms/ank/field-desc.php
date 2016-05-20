<?php

define('XSM_SCHOOL_ANK_ID', 'ank');

// field types
define('XSM_FT_FOREIGN_KEY', 'fk');
define('XSM_FT_STR', 'input');
define('XSM_FT_TEXT', 'textarea');
define('XSM_FT_ENUM', 'enum');
define('XSM_FT_CHECKBOX', 'checkbox');

// new style field descriptors
function xsm_get_fields($table_name)
{
    $field_desc = xsm_get_all_field_descriptors();
    return $field_desc[$table_name];
}

function xsm_get_all_field_descriptors()
{
    $field_descriptors = array(

        // department
        "department"=>array(
            "department_title"=>array(
                "name"=>"Название",
                "type"=>XSM_FT_STR,
                "required"=>true,
            ),
        ),

        // school
        "school"=>array(
            "school_title"=>array(
                "name"=>"Название",
                "type"=>XSM_FT_STR,
                "required"=>true,
            ),
            "school_type"=>array(
                "name"=>"Тип",
                "type"=>XSM_FT_ENUM,
            ),
            "school_date_start"=>array(
                "name"=>"Дата начала (ГГГГ.ММ.ДД)",
                "type"=>XSM_FT_STR,
            ),
            "school_date_end"=>array(
                "name"=>"Дата окончания (ГГГГ.ММ.ДД)",
                "type"=>XSM_FT_STR,
            ),
            "school_location"=>array(
                "name"=>"Место проведения",
                "type"=>XSM_FT_STR,
            ),
        ),

        // person
        "person"=>array(
            "department_id"=>array(
                "name"=>"Отделение",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "anketa_status"=>array(
                "name"=>"Статус",
                "type"=>XSM_FT_ENUM,
            ),
            "last_name"=>array(
                "name"=>"Фамилия",
                "type"=>XSM_FT_STR,
                "required"=>true,
            ),
            "first_name"=>array(
                "name"=>"Имя",
                "type"=>XSM_FT_STR,
                "required"=>true,
            ),
            "patronymic"=>array(
                "name"=>"Отчество",
                "type"=>XSM_FT_STR,
            ),
            "nick_name"=>array(
                "name"=>"Ник",
                "type"=>XSM_FT_STR,
            ),
            "birth_date"=>array(
                "name"=>"Дата рождения",
                "type"=>XSM_FT_STR,
            ),
            "passport_data"=>array(
                "name"=>"Паспортные данные",
                "type"=>XSM_FT_STR,
            ),
            "school"=>array(
                "name"=>"Школа",
                "type"=>XSM_FT_STR,
            ),
            "school_city"=>array(
                "name"=>"Адрес школы",
                "type"=>XSM_FT_STR,
            ),
            "ank_class"=>array(
                "name"=>"Класс подачи анкеты",
                "type"=>XSM_FT_STR,
            ),
            "current_class"=>array(
                "name"=>"Класс",
                "type"=>XSM_FT_STR,
            ),
            "phone"=>array(
                "name"=>"Телефон",
                "type"=>XSM_FT_STR,
            ),
            "cellular"=>array(
                "name"=>"Мобильный телефон",
                "type"=>XSM_FT_STR,
            ),
            "email"=>array(
                "name"=>"E-Mail",
                "type"=>XSM_FT_STR,
            ),
            "skype"=>array(
                "name"=>"Skype",
                "type"=>XSM_FT_STR,
            ),
            "social_profile"=>array(
                "name"=>"Профиль в соц. сети",
                "type"=>XSM_FT_STR,
            ),
            "is_teacher"=>array(
                "name"=>"Препод",
                "type"=>XSM_FT_CHECKBOX,
            ),
            "is_student"=>array(
                "name"=>"Школьник",
                "type"=>XSM_FT_CHECKBOX,
            ),
            "tent_capacity"=>array(
                "name"=>"Вместимость палатки",
                "type"=>XSM_FT_STR,
            ),
            "tour_requisites"=>array(
                "name"=>"Туристское барахло",
                "type"=>XSM_FT_TEXT,
            ),
            "forest_1"=>array(
                "name"=>"1-й выход в лес",
                "type"=>XSM_FT_ENUM,
            ),
            "forest_2"=>array(
                "name"=>"2-й выход в лес",
                "type"=>XSM_FT_ENUM,
            ),
            "forest_3"=>array(
                "name"=>"3-й выход в лес",
                "type"=>XSM_FT_ENUM,
            ),
            "favourites"=>array(
                "name"=>"Любимые предметы",
                "type"=>XSM_FT_TEXT,
            ),
            "achievements"=>array(
                "name"=>"Достижения",
                "type"=>XSM_FT_TEXT,
            ),
            "hobby"=>array(
                "name"=>"Хобби",
                "type"=>XSM_FT_TEXT,
            ),
            "lesh_ref"=>array(
                "name"=>"Откуда узнали о школе",
                "type"=>XSM_FT_TEXT,
            ),
            "user_agent"=>array(
                "name"=>"UserAgent",
                "type"=>XSM_FT_STR,
                "readonly"=>true,
            ),
        ),

        // person on school
        "person_school"=>array(
            "member_person_id"=>array(
                "name"=>"Участник",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "school_id"=>array(
                "name"=>"Школа",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "member_department_id"=>array(
                "name"=>"Отделение",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "is_student"=>array(
                "name"=>"Школьник",
                "type"=>XSM_FT_CHECKBOX,
            ),
            "current_class"=>array(
                "name"=>"Класс",
                "type"=>XSM_FT_STR,
            ),
            "courses_needed"=>array(
                "name"=>"Потребное кол-во зачётов",
                "type"=>XSM_FT_STR,
            ),
            "curator_group"=>array(
                "name"=>"Кто курирует",
                "type"=>XSM_FT_STR,
            ),
            "is_teacher"=>array(
                "name"=>"Препод",
                "type"=>XSM_FT_CHECKBOX,
            ),
            "curatorship"=>array(
                "name"=>"Кураторство",
                "type"=>XSM_FT_ENUM,
            ),
            "person_school_comment"=>array(
                "name"=>"Комментарий",
                "type"=>XSM_FT_TEXT,
            ),
        ),

        // person_comment
        "person_comment"=>array(
            "comment_text"=>array(
                "name"=>"Текст комментария",
                "type"=>XSM_FT_TEXT,
                "required"=>true,
            ),
            "owner_login"=>array(
                "name"=>"Логин автора",
                "readonly"=>true,
                "type"=>XSM_FT_STR,
            ),
            "blamed_person_id"=>array(
                "name"=>"ID субъекта",
                "readonly"=>true,
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            // TODO: internals
            "person_comment_deleted"=>array(
                "name"=>"Объект удалён",
                "type"=>XSM_FT_ENUM,
                "hidden"=>true,
            ),
        ),

        // course
        "course"=>array(
            "course_title"=>array(
                "name"=>"Название курса",
                "type"=>XSM_FT_STR,
            ),
            "target_class"=>array(
                "name"=>"Уровень (диапазон классов)",
                "type"=>XSM_FT_STR,
            ),
            "school_id"=>array(
                "name"=>"Школа, на которой читался курс",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "course_cycle"=>array(
                "name"=>"Цикл, на котором читался курс",
                "type"=>XSM_FT_STR,
            ),
            "course_desc"=>array(
                "name"=>"Описание",
                "type"=>XSM_FT_TEXT,
            ),
            "course_type"=>array(
                "name"=>"Тип курса",
                "type"=>XSM_FT_ENUM,
            ),
            "course_area"=>array(
                "name"=>"Тематика",
                "type"=>XSM_FT_ENUM,
            ),
            "course_comment"=>array(
                "name"=>"Комментарий",
                "type"=>XSM_FT_TEXT,
            ),
        ),

        // course teachers
        "course_teachers"=>array(
            "course_id"=>array(
                "name"=>"Курс",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "course_teacher_id"=>array(
                "name"=>"Препод курса",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
        ),

        // exam
        "exam"=>array(
            "student_person_id"=>array(
                "name"=>"Школьник",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "course_id"=>array(
                "name"=>"Курс",
                "type"=>XSM_FT_FOREIGN_KEY,
            ),
            "exam_status"=>array(
                "name"=>"Состояние",
                "type"=>XSM_FT_ENUM,
            ),
            "deadline_date"=>array(
                "name"=>"Дедлайн",
                "type"=>XSM_FT_STR,
            ),
            "exam_comment"=>array(
                "name"=>"Комментарий к зачёту",
                "type"=>XSM_FT_TEXT,
            ),
        ),

    );

    foreach ($field_descriptors as $object_type => $fields_desc) {
        $field_descriptors[$object_type]["${object_type}_created"] = array(
            "name"=>"Дата создания",
            "type"=>XSM_FT_STR,
            "readonly"=>true,
        );
        $field_descriptors[$object_type]["${object_type}_modified"] = array(
            "name"=>"Последняя модификация",
            "type"=>XSM_FT_STR,
            "readonly"=>true,
        );
    }

    return $field_descriptors;
}

global $XSM_ENUMS;

// статус анкеты (значения в базе)
$XSM_ENUMS["anketa_status"] = array(
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
        "spam"=>"Спам",
    ),
    "default"=>"new",
);

// селектор для list-person-locator
$XSM_ENUMS["show_anketa_status_locator"] = array(
    "values"=>array(
        "active"=>"Актив",
        "no-trash"=>"Все",
        "not-decl"=>"Все, кроме посланных",
        "not-old"=>"Все, кроме архивных",
        "processed"=>"Принятые",
        "cont"=>"Продолжающие",
        "old"=>"Архивные",
        "all"=>"Без фильтрации"),
    "default"=>"active",
);

// селектор для list-ank
$XSM_ENUMS["show_anketa_status_ank"] = array(
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
        "all"=>"Без фильтрации",
    ),
    "default"=>"abitur",
);

// Статус выхода в лес
$XSM_ENUMS["forest_status"] = array(
    "values"=>array(
        "undef"=>"&mdash;",
        "notable"=>"Не может",
        "no"=>"Не идёт",
        "maybe"=>"ХЗ",
        "able"=>"Может",
        "yes"=>"Идёт",
    ),
    "default"=>"undef",
);

// Фильтр для показов выходов в лес
$XSM_ENUMS["show_forest_num"] = array(
    "values"=>array(
        "all"=>"Все выходы",
        "forest_1"=>"1-й выход",
        "forest_2"=>"2-й выход",
        "forest_3"=>"3-й выход",
    ),
    "default"=>"all",
);

// Кураторство
$XSM_ENUMS["curatorship"] = array(
    "values"=>array(
        "none"=>"Не куратор",
        "assist"=>"Помощник куратора",
        "cur"=>"Куратор",
    ),
    "default"=>"none",
);

// Зачёт
$XSM_ENUMS["exam_status"] = array(
    "values"=>array(
        "listen"=>"Прослушан",
        "passed"=>"Сдан",
        "notpassed"=>"Не сдан",
        "almost"=>"Почти сдан",
        "other"=>"Иное"),
    "default"=>"listen",
);

// Тип школы
$XSM_ENUMS["school_type"] = array(
    "values"=>array(
        "lesh"=>"Летняя",
        "zesh"=>"Зимняя",
        "vesh"=>"Весеннняя",
    ),
    "default"=>"lesh",
);

// Тип курса
$XSM_ENUMS["course_type"] = array(
    "values"=>array(
        "generic"=>"Обычный",
        "facult"=>"Факультатив",
        "prac"=>"Практикум",
        "single"=>"Разовая лекция",
        "other"=>"Иное",
    ),
    "default"=>"generic",
);

// Тематика курса
$XSM_ENUMS["course_area"] = array(
    "values"=>array(
        "unknown"=>"Не выбрано",
        "precise"=>"Точные науки",
        "cs"=>"Computer science",  // #864
        "nature"=>"Естественные науки",
        "human"=>"Гуманитарные науки",
        "other"=>"Иное",
    ),
    "default"=>"unknown",
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

function xsm_saved_form($table_name)
{
    $forms = array(
        'school'=>'сохранена',
        'department'=>'сохранено',
    );
    return xcms_get_key_or($forms, $table_name, 'сохранён');
}

function xsm_field_desc_unit_test()
{
    xut_begin("field-desc");
    $field_descriptors = xsm_get_all_field_descriptors();
    foreach ($field_descriptors as $object_type => $fields_desc) {
        foreach ($fields_desc as $field_name => $field_desc) {
            $type = xcms_get_key_or($field_desc, "type");
            xut_check(!xu_empty($type), "Type $object_type::$field_name should not be empty");
        }
    }
    xut_end();
}

?>