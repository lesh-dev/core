-- unused part of dbinit section and samples

create table exam_attempt (
    exam_attempt_id integer primary key autoincrement,
    student_person_id integer not null, -- fk
    course_id integer not null, -- fk
    attempt_date text,
    foreign key (student_person_id) references person(person_id),
    foreign key (course_id) references course(course_id)
);

insert into person (last_name, first_name, patronymic,
    birth_date,
    school, school_city,
    phone, cellular, email, skype,
    is_teacher, person_created) values
    ('Вельтищев', 'Михаил', 'Николаевич',
    '2012.05.06',
    '444', 'Москва',
    '+7 (495) 618 30 21', '+7 (915) 0-686-186', 'dichlofos-mv@yandex.ru', 'dichlofos.mv',
    'teacher', '2012.05.07 03:05:01');

insert into person (last_name, first_name, patronymic, is_teacher, person_created, person_modified)
    values ('Вельтищев', 'Дмитрий', 'Николаевич', 'teacher', '2012.05.07 03:05:01', '2012.06.10 01:02:03');

insert into person (last_name, first_name, patronymic, is_student, person_created, person_modified)
    values ('Школьница', 'Мария', 'Батьковна', 'student', '2012.01.04 03:05:01', '2012.05.01 01:05:01');

insert into person (last_name, first_name, patronymic, is_student, person_created, person_modified)
    values ('Школьница2', 'Мария2', 'Батьковна2', 'student', '2012.01.04 03:05:01', '2012.05.01 01:05:01');

insert into course (course_title, course_teacher_id, target_class, course_desc) values
    ('Хрень какая-то', 1, '10-11', 'Сами прочитайте в книжке');

insert into course (course_title, course_teacher_id, target_class, course_desc) values
    ('Дрянь1', 2, '10-11', 'Сами прочитайте в книжке Б');
insert into course (course_title, course_teacher_id, target_class, course_desc) values
    ('Дрянь2', 2, '8-11', 'Сами прочитайте в книжке А');
insert into course (course_title, course_teacher_id, target_class, course_desc) values
    ('Дрянь3', 2, '11', 'Сами!');

insert into exam (student_person_id, course_id, exam_status)
    values (3, 1, 'passed');
insert into exam (student_person_id, course_id, exam_status)
    values (3, 2, 'passed');

insert into exam (student_person_id, course_id, exam_status)
    values (4, 1, 'passed');
insert into exam (student_person_id, course_id, exam_status)
    values (4, 2, 'passed');
insert into exam (student_person_id, course_id, exam_status)
    values (4, 3, 'passed');


select * from person;
select * from course;

