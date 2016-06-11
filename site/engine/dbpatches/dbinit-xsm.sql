/* Версия базы данных (2.13+) */
create table xversion (
    db_version text
);

insert into xversion values('0.0.0');
update `xversion` set db_version = '2.13.1';

/* Отделение (2.7+) */
create table department (
    department_id integer primary key autoincrement,
    department_title text,
    department_created text, -- utc timestamp
    department_modified text, -- utc timestamp
    department_changedby text -- user name
);

/* Not to deal with #818 */
insert into department (department_title, department_created, department_changedby) values ('Физическое', '2005.08.23 01:02:03', 'serge');

/* Участник (препод, куратор, школьник...) */
create table person (
    person_id integer primary key autoincrement,

    last_name text, -- фамилия
    first_name text, -- имя
    patronymic text, -- отчество
    nick_name text, -- кличка #569

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

    department_id integer not null, -- ссылка на отделение (2.7+)

    person_created text, -- utc timestamp
    person_modified text, -- utc timestamp
    person_changedby text, -- user name

    foreign key (department_id) references department(department_id)
);

/* Курс */
create table course (
    course_id integer primary key autoincrement,
    course_title text, -- название курса
    school_id integer not null, -- ссылка на школу, на которой читали курс
    course_cycle text,  -- цикл, на котором читался курс
    target_class text, -- диапазон классов, на которые рассчитан курс
    course_desc text,  -- описание курса
    course_type text, --- enum тип курса (прак, поход, etc)
    course_area text, --- enum предметная область
    course_comment text, -- комментарий к курсу (чатик пока не делаем)
    course_created text, -- utc timestamp
    course_modified text, -- utc timestamp
    course_changedby text -- user name
);

/* Преподы курсов (2.4+) */
create table course_teachers (
    course_teachers_id integer primary key autoincrement,
    course_id integer not null, -- fk
    course_teacher_id integer not null, -- fk
    course_teachers_created text, -- utc timestamp
    course_teachers_modified text, -- utc timestamp
    course_teachers_changedby text, -- user name
    foreign key (course_id) references course(course_id),
    foreign key (course_teacher_id) references person(person_id)
);

/* Зачёт */
create table exam (
    exam_id integer primary key autoincrement, -- not used
    student_person_id integer not null, -- fk
    course_id integer not null, -- fk
    exam_status text,
    deadline_date text,
    exam_comment text,
    exam_created text, -- utc timestamp
    exam_modified text, -- utc timestamp
    exam_changedby text, -- user name
    foreign key (student_person_id) references person(person_id),
    foreign key (course_id) references course(course_id)
);

/* Школа */
create table school (
    school_id integer primary key autoincrement,
    school_title text,
    school_type text, -- enum:(летняя, зимняя)
    school_date_start text, -- дата начала
    school_date_end text, -- дата конца
    school_location text, -- место проведения (2.7+)
    school_created text, -- utc timestamp
    school_modified text, -- utc timestamp
    school_changedby text -- user name
);

/*
Связка "Бытие участника на школе"

Роли человека на школе и его принадлежность к отделению
по умолчанию копируются из его профиля.

Именно в этой связке должна быть проставлена роль участника
на данной школе (на одной школе он был школьником,
а на следующей школе он был уже преподом и куратором).

В этой же таблице хранится принадлежность препода к отделению
относительно данной школы.
*/
create table person_school (
    person_school_id integer primary key autoincrement,
    member_person_id integer not null, -- fk person
    member_department_id integer not null, -- fk department
    school_id integer not null, -- fk school
    is_student text, -- является ли школьником на данной школе
    is_teacher text, -- является ли преподом на данной школе
    curatorship text, -- кураторство на данной школе enum:(никто, помкур, куратор)
    curator_group text, -- группа кураторства
    current_class text, -- класс, в котором находится школьник
        -- (для Летней школы надо договориться, какой именно класс мы ставим,
        -- будущий или прошедший
    courses_needed integer, -- потребное кол-во курсов для сдачи на школе
    person_school_comment text, -- комментарий (v2.10)
    person_school_created text, -- utc timestamp
    person_school_modified text, -- utc timestamp
    person_school_changedby text, -- user name
    foreign key (member_person_id) references person(person_id),
    foreign key (member_department_id) references department(department_id),
    foreign key (school_id) references school(school_id)
);

/*
Комментарии относительно участника (типично школьника)
(чатик при наборе и поведении на школе)
*/
create table person_comment (
    person_comment_id integer primary key autoincrement,
    comment_text text, -- текст комментария
    blamed_person_id integer not null, -- fk person -- сабжевый участник (типично школьник)
    -- school_id integer not null, -- fk school -- школа, о которой идёт речь
    owner_login text not null, -- логин автора комментария
    -- owner_person_id integer not null, -- fk person -- владелец комментария (типично препод)
    person_comment_created text, -- utc timestamp
    person_comment_modified text, -- utc timestamp
    person_comment_deleted text, -- признак удаления (из базы ничего удалить нельзя)
    person_comment_changedby text, -- user name
    foreign key (blamed_person_id) references person(person_id)
    -- foreign key (school_id) references school(school_id),
    -- foreign key (owner_person_id) references person(person_id)
);
