/* Преподы курсов */
create table course_teachers (
    course_teachers_id integer primary key autoincrement,
    course_id integer not null, -- fk
    course_teacher_id integer not null, -- fk
    foreign key (course_id) references course(course_id),
    foreign key (course_teacher_id) references person(person_id)
);