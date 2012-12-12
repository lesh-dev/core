-- drop table if exists exam_attempt;
drop table if exists exam;
drop table if exists course;
drop table if exists person;

create table person (
    person_id integer primary key autoincrement,

    last_name text,
    first_name text,
    patronymic text,

    birth_date text,
    passport_data text,

    school text,
    school_city text,
    current_class text,

    phone text,
    cellular text,
    email text,
    skype text,
    social_profile text,

    is_teacher text,
    is_student text,
    curatorship text,

    favourites text,
    achievements text,
    hobby text,

    activity_status text, -- former anketa status
    is_current text, -- присутствует ли на текущем мероприятии

    person_comment text,
    user_agent text,

    person_created text, -- utc timestamp -- rename
    person_modified text -- utc timestamp
);

create table course (
    course_id integer primary key autoincrement,
    course_title text,
    course_teacher_id integer not null,
    target_class text, -- диапазон классов, на которые рассчитан курс
    course_desc text,
    course_comment text,
    course_created text, -- utc timestamp -- rename
    course_modified text, -- utc timestamp
    foreign key(course_teacher_id) references person(person_id)
);

create table exam (
    exam_id integer primary key autoincrement, -- not used
    student_person_id integer not null, -- fk
    course_id integer not null, -- fk
    exam_status text,
    deadline_date text,
    is_prac text, -- enum
    exam_comment text,
    exam_created text,
    exam_modified text,
    foreign key (student_person_id) references person(person_id),
    foreign key (course_id) references course(course_id)
);
