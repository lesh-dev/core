-- 1
insert into person (last_name, first_name, patronymic,
    birth_date,
    school, school_city, ank_class,
    is_teacher, is_student,
    phone, cellular, email, skype,
    social_profile,
    anketa_status, person_created) values
    ('Вельтищев1', 'Михаил', 'Николаевич',
    '2012.05.06',
    '444', 'Москва', '9г',
    'teacher', '',
    '+7 (495) 618 30 21', '+7 (915) 0-686-186', 'dichlofos-mv@yandex.ru', 'dichlofos.mv',
    'http://vk.com/dichlofos',
    'cont', '2012.05.07 03:05:01');
-- 2
insert into person (last_name, first_name, patronymic, anketa_status, is_teacher, person_created, person_modified)
    values ('Вельтищев2', 'Дмитрий', 'Николаевич', 'cont', 'teacher', '2012.05.07 03:05:01', '2012.06.10 01:02:03');
-- 3
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Школьница3', 'Мария-3', 'Батьковна', 'processed', 'student', '2012.01.04 03:05:01', '2012.05.01 01:05:01');
-- 4
insert into person (last_name, first_name, patronymic, anketa_status, is_student, ank_class, school_city, person_created, person_modified)
    values ('Школьница4', 'Мария', 'Батьковна', 'processed', 'student', '10a', 'Default City of USA', '2012.01.04 03:05:01', '2012.05.01 01:05:01');
-- 5
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Школьница5', 'Мария2', 'Батьковна2', 'cont', 'student', '2012.01.04 03:05:01', '2012.05.01 01:05:01');
-- 6
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Школьница6', 'Настоящая', 'Михайловна', 'cont', 'student', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 7
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Школьница7', 'Настоящая', 'Ивановна', 'cont', 'student', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 8
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Новобранец8', 'ТолькоЧто', 'Хреновый', 'new', '', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 9
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Ветеран9', 'ДавноУже', 'НеШкольник', 'cont', 'student', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 10
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Новобранец10', 'ТолькоЧто2', 'Школьник2', 'processed', '', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 11
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Приглашённый2', 'ТолькоЧто3', 'Школьник3', 'progress', '', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 12
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Приглашённый2', 'ТолькоЧто3', 'Школьник3', 'progress', '', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 13
insert into person (last_name, first_name, patronymic, anketa_status, is_student, person_created, person_modified)
    values ('Посланный1', 'Намедни', 'Школьник4', 'declined', '', '2012.01.04 04:01:02', '2012.06.01 01:05:01');
-- 14
insert into person (last_name, first_name, patronymic, anketa_status, is_teacher, person_created, person_modified)
    values ('Трусевич1', 'Александр', 'Николаевич', 'cont', 'teacher', '2012.05.07 03:05:01', '2012.06.10 01:02:03');

insert into school values(1, 'ЛЭШ-2011', 'summmer', '2011.07.23', '2011.08.22', null, null);
insert into school values(2, 'ЗЭШ-2012', 'winter', '2012.01.02', '2012.01.09', null, null);
insert into school values(3, 'ЗЭШ-2010', 'winter', '2010.01.02', '2010.01.09', null, null);

--                               id,  mem, sch, is_st,     is_t,      cur,  cls,   cn
insert into person_school values(1,   1,   1,   null,      'teacher', null, 'мм',  '2', null, null);
insert into person_school values(2,   1,   2,   null,      'teacher', null, 'вмк', '2', null, null);
insert into person_school values(3,   2,   1,   null,      'teacher', null, 'мм',  '8', null, null);
insert into person_school values(4,   2,   2,   null,      'teacher', null, 'вмк', '8', null, null);
insert into person_school values(5,   3,   1,   'student', null,      null, '9',   '8', null, null);
insert into person_school values(6,   3,   2,   'student', null,      null, '10',  '8', null, null);
insert into person_school values(7,   4,   2,   null,      'teacher', null, '9',   '8', null, null);
insert into person_school values(8,   5,   2,   null,      'teacher', null, '8',   '8', null, null);
insert into person_school values(9,   6,   2,   'student', null,      null, '7',   '8', null, null);
insert into person_school values(10,  7,   2,   'student', 'teacher', null, '11',  '8', null, null);
insert into person_school values(11,  9,   3,   '',        null,      null, '11ж', '8', null, null);
insert into person_school values(12, 14,   3,   '',        'teacher', null, '5к',  '8', null, null);

--                        id, title,              sch, cyc,  tch,    cl
insert into course values(1, 'test course',       1,    '1',   1,  '7-9',  'тестовый курс для болванов',    'comm1',      't666', 'aaa');
insert into course values(2, 'not a Test course', 1,  '1-2',   2,   '9+',  'то же самое, только в профиль', 'comment 2',  't666', 'aaa');
insert into course values(3, 'Вынос мозга',       2,    '3',   2,  '10+',  'не для болванов',               'comment 3',  't666', 'aaa');
insert into course values(4, 'Пайтон',            2,    '3',   2,   '6+',  'Школота схавает',               'comment 4',  't666', 'aaa');
insert into course values(5, 'Хрень, а не курс',  2,    '4',   2,  '6-8',  'Как вязать крючком',            'comment 5',  't666', 'aaa');
insert into course values(6, 'Дыры в PHP',        2,  '2-3',  14,   '8+',  'Kernel PHP hacking',            'comment 10', 't666', 'aaa');
--                         stu, crs
insert into exam values(1, 4,   1,  'passed', 'qqq2',  'qqq3',    'qqq4', 'qqq5', 'aaaa');
insert into exam values(2, 5,   2,  'passed', 'qqq21', 'qqq330',  'qqq4', 'qqq5', 'bbb');
insert into exam values(3, 5,   3,  'failed', 'qqq22', 'qqq34-',  'qqq4', 'qqq5', 'ccc');
insert into exam values(4, 5,   4,  'failed', 'qqq23', 'qqq35--', 'qqq4', 'qqq5', 'ddd');
insert into exam values(5, 6,   2,  'passed', 'qqq23', 'qqq35--', 'qqq4', 'qqq5', 'ddd');
insert into exam values(6, 6,   4,  'passed', 'qqq23', 'qqq35--', 'qqq4', 'qqq5', 'ddd');
insert into exam values(7, 6,   5,  'passed', 'qqq23', 'qqq35--', 'qqq4', 'qqq5', 'ddd');

-- notbound students
SELECT * FROM person p LEFT JOIN person_school ps ON p.person_id = ps.member_person_id WHERE ps.member_person_id IS NULL;
