drop table if exists exam;
drop table if exists course;
drop table if exists person;

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
    current_class text, -- класс подачи заявки

    phone text,         -- телефон (городской)
    cellular text,      -- мобильный телефон
    email text,         -- контактный email
    skype text,         -- skype
    social_profile text,  -- профиль ВКонтакте и т.п. (используемый!)

    is_teacher text, -- типично препод
    is_student text, -- типично школьник
    curatorship text, -- типично куратор ?

    favourites text,     -- любимые предметы
    achievements text,   -- достижения
    hobby text,          -- хобби

    activity_status text, -- former anketa status
    is_current text, -- присутствует ли на текущем мероприятии
    person_comment text, -- комментарий о человеке
    user_agent text,    -- идентификатор браузера, с которого была подана анкета

    person_created text, -- utc timestamp
    person_modified text -- utc timestamp
);

/* Курс */
create table course (
    course_id integer primary key autoincrement,
    course_title text, -- название курса
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
