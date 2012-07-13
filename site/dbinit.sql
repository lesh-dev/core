drop table if exists exam_attempt;
drop table if exists exam;
drop table if exists course;
drop table if exists person;

create table person (
    person_id integer primary key autoincrement,
    last_name text,
    first_name text,
    patronymic text,

    birth_date text,
    entrance_class text,

    school text,
    school_city text,

    phone text,
    cellular text,
    email text,
    skype text,

    -- passport data

    social_profile text,

    favourites text,
    hobby text,

    acttivity_status text, -- active or former
    role text,

    is_teacher text,
    is_curator text,

    created text, -- utc timestamp
    modified text -- utc timestamp
);

create table course (
    course_id integer primary key autoincrement,
    title text,
    teacher_person_id integer not null,
    target_class text, -- диапазон классов, на которые рассчитан курс
    description text,
    comment text,
    foreign key(teacher_person_id) references person(person_id)
);


create table exam (
    exam_id integer primary key autoincrement, -- not used
    student_person_id integer not null, -- fk
    course_id integer not null, -- fk
    exam_status text,
    deadline_date text,
    is_prac text, -- enum
    comment text,
    foreign key (student_person_id) references person(person_id),
    foreign key (course_id) references course(course_id)
);

create table exam_attempt (
    exam_attempt_id integer primary key autoincrement,
    student_person_id integer not null, -- fk
    course_id integer not null, -- fk
    attempt_date text,
    foreign key (student_person_id) references person(person_id),
    foreign key (course_id) references course(course_id)
);


insert into person (last_name, first_name, patronymic, school, school_city, email, skype, is_teacher, created)
    values ('Вельтищев', 'Михаил', 'Николаевич', '444', 'Москва', 'dichlofos-mv@yandex.ru', 'dichlofos.mv', 'teacher', '2012.05.07 03:05:01');
insert into person (last_name, first_name, patronymic, is_teacher, created, modified)
    values ('Вельтищев', 'Дмитрий', 'Николаевич', 'teacher', '2012.05.07 03:05:01', '2012.06.10 01:02:03');
insert into person (last_name, first_name, patronymic, is_teacher, created, modified)
    values ('Школьница', 'Мария', 'Батьковна', 'student', '2012.01.04 03:05:01', '2012.05.01 01:05:01');

insert into course (title, teacher_person_id, target_class, description) values
    ('Хрень какая-то', 1, '10-11', 'Сами прочитайте в книжке');

insert into course (title, teacher_person_id, target_class, description) values
    ('Дрянь1', 2, '10-11', 'Сами прочитайте в книжке Б');
insert into course (title, teacher_person_id, target_class, description) values
    ('Дрянь2', 2, '8-11', 'Сами прочитайте в книжке А');

select * from person;
select * from course;
