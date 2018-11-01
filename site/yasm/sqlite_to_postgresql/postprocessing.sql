SELECT pg_catalog.set_config('search_path', 'public', false);

SELECT setval('contact_id_seq', (SELECT max(id) FROM contact));
SELECT setval('contestants_contestants_id_seq', (SELECT max(contestants_id) FROM contestants));
SELECT setval('course_course_id_seq', (SELECT max(course_id) FROM course));
SELECT setval('course_teachers_course_teachers_id_seq', (SELECT max(course_teachers_id) FROM course_teachers));
SELECT setval('department_department_id_seq', (SELECT max(department_id) FROM department));
SELECT setval('exam_exam_id_seq', (SELECT max(exam_id) FROM exam));
SELECT setval('notification_notification_id_seq', (SELECT max(notification_id) FROM notification));
SELECT setval('person_person_id_seq', (SELECT max(person_id) FROM person));
SELECT setval('person_comment_person_comment_id_seq', (SELECT max(person_comment_id) FROM person_comment));
SELECT setval('person_school_person_school_id_seq', (SELECT max(person_school_id) FROM person_school));
SELECT setval('problems_problems_id_seq', (SELECT max(problems_id) FROM problems));
SELECT setval('school_school_id_seq', (SELECT max(school_id) FROM school));
SELECT setval('solutions_solutions_id_seq', (SELECT max(solutions_id) FROM solutions));
SELECT setval('submission_submission_id_seq', (SELECT max(submission_id) FROM submission));
