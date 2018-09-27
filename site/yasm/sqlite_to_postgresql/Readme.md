Процедура переноса данных.

fizlesh.sqlite3 -- исходная база.
pgloader версии 3.4.1 compiled with SBCL1.3.1.debian

1. Чистим битые ссылки и кривые целые числа:
    
    sqlite3> delete from course_teachers where not exists (select * from course where course.course_id = course_teachers.course_id) or not exists (select * from person where person_id = course_teachers.course_teacher_id);
             delete from exam where not exists (select * from course where course.course_id = exam.course_id) or not exists (select * from person where person_id = student_person_id);
             UPDATE person_comment SET school_id = NULL WHERE school_id = '';
2. Переносим схему:

    ./pgloader 1_schema.load
3. Меняем тип integer-колонки со значениями вида '2 + прак'

    psql> ALTER TABLE person_school ALTER COLUMN courses_needed TYPE varchar;
4. Переносим данные:

    ./pgloader 2_data.sql
    
    Будет много ошибок на person_comment, person_school.
5. Чистим эти таблицы, чтобы накатить их руками:

    psql> TRUNCATE person_school; TRUNCATE person_comment;
6. Экспортируем их:

    sqlite3 fizlesh.sqlite3 '.dump person_school' > /tmp/person_school.sql
    
    sqlite3 fizlesh.sqlite3 '.dump person_comment' > /tmp/person_comment.sql
    
    sqlite3 fizlesh.sqlite3 '.dump course_teachers' > /tmp/course_teachers.sql
    
    Убираем из начала файлов прагму и ddl.
7. Импортируем:

    psql -f /tmp/person_school.sql
    
    psql -f /tmp/person_comment.sql
    
    psql -f /tmp/course_teachers.sql