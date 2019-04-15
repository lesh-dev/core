
delete from course_teachers where
    not exists (
        select * from course where course.course_id = course_teachers.course_id
    ) or
    not exists (
        select * from person where person_id = course_teachers.course_teacher_id
    );

delete from exam where
    not exists (
        select * from course where course.course_id = exam.course_id
    ) or
    not exists (
        select * from person where person_id = student_person_id
    );

UPDATE person_comment  SET school_id =                NULL WHERE school_id = '';
UPDATE course          SET course_modified =          NULL WHERE course_modified = '';
UPDATE course_teachers SET course_teachers_modified = NULL where course_teachers_modified = '';
UPDATE exam            SET exam_modified =            NULL WHERE exam_modified = '';
UPDATE person          SET person_modified =          NULL WHERE person_modified = '';
UPDATE person_comment  SET person_comment_modified =  NULL WHERE person_comment_modified = '';
UPDATE person_school   SET person_school_modified =   NULL WHERE person_school_modified = '';
UPDATE school          SET school_modified =          NULL WHERE school_modified = '';
UPDATE school          SET school_created =           NULL WHERE school_created = '';
