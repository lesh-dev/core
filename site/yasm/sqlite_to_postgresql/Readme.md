Процедура переноса данных.

../fizlesh.sqlite3 -- исходная база.
pgloader версии 3.4.1 compiled with SBCL1.3.1.debian
(использовался для генерации схемы, для миграции не нужен).

1. Чистим битые ссылки и кривые целые числа:
    
    sqlite3> delete from course_teachers where not exists (select * from course where course.course_id = course_teachers.course_id) or not exists (select * from person where person_id = course_teachers.course_teacher_id);
             delete from exam where not exists (select * from course where course.course_id = exam.course_id) or not exists (select * from person where person_id = student_person_id);
             UPDATE person_comment SET school_id = NULL WHERE school_id = '';
2. Запускаем `./migrate.sh`.
