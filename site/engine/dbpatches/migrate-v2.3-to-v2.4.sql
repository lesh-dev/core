alter table course add column course_teacher_item integer;

/* Преподы курсов */
create table course_teacher (
    course_teacher_id integer primary key autoincrement,
    course_teacher_item integer not null,
    teacher_id not null -- fk
);
