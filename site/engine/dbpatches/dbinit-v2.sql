drop table if exists exam;
drop table if exists course;
drop table if exists person_school;
drop table if exists person;
drop table if exists school;

/* Участник (препод, куратор, школьник...) */
create table person (
    person_id integer primary key autoincrement,

    last_name text, -- фамилия
    first_name text, -- имя
    patronymic text, -- отчество

    birth_date text, -- дата рождения
    passport_data text, -- паспортные данные

    school text,        -- школа, в которой учится школьник
    school_city text,   -- город, в котором находится школа
    ank_class text, -- класс подачи заявки

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

    anketa_status text, -- former activity_status
        -- enum:(new, processed, declined, taken, duplicated, spam)

    user_agent text,    -- идентификатор браузера, с которого была подана анкета

    person_created text, -- utc timestamp
    person_modified text -- utc timestamp
);

/* Курс */
create table course (
    course_id integer primary key autoincrement,
    course_title text, -- название курса
    school_id integer not null, -- ссылка на школу, на которой читали курс
    course_cycle text,  -- цикл, на котором читался курс
    course_teacher_id integer not null, -- ссылка на препода
    target_class text, -- диапазон классов, на которые рассчитан курс
    course_desc text,  -- описание курса
    course_comment text, -- комментарий к курсу (чатик пока не делаем)
    course_created text, -- utc timestamp
    course_modified text, -- utc timestamp
    foreign key(course_teacher_id) references person(person_id)
);

/* Зачёт */
create table exam (
    exam_id integer primary key autoincrement, -- not used
    student_person_id integer not null, -- fk
    course_id integer not null, -- fk
    exam_status text,
    deadline_date text,
    is_prac text, -- enum -- ой, зачем же это в свойствах зачёта? это же свойство курса!
    exam_comment text,
    exam_created text,
    exam_modified text,
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
    school_created text, -- utc timestamp
    school_modified text -- utc timestamp
);

/*
Связка "Бытие участника на школе"

Роль человека на школе по умолчанию копируется из

Именно в этой связке должна быть проставлена роль участника на школе
(на одной школе он был школьником, на школе следующей он был уже преподом)
Таким образом, статусы is_student, is_teacher, curatorship участника
переезжают сюда.

TODO добавить место проведения школы
*/
create table person_school (
    person_school_id integer primary key autoincrement,
    member_person_id integer not null, -- fk person
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
    foreign key (blamed_person_id) references person(person_id)
    -- foreign key (school_id) references school(school_id),
    -- foreign key (owner_person_id) references person(person_id)
);
