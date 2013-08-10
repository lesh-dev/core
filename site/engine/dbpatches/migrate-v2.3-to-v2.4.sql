/* Преподы курсов */
create table course_teachers (
    course_teachers_id integer primary key autoincrement,
    course_id integer not null, -- fk
    course_teacher_id integer not null, -- fk
    course_teachers_created text, -- utc timestamp
    course_teachers_modified text -- utc timestamp
    foreign key (course_id) references course(course_id),
    foreign key (course_teacher_id) references person(person_id)
);