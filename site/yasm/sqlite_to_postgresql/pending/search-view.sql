-- TODO: возможно, сделать summary (json) и title перенести туда
-- TODO: по каким сущностям надо искать? Комментарии, заявки, ещё?
-- TODO: сниппеты (скорее на фронте)
CREATE VIEW search(source, id, title, description) AS WITH
    courses AS (SELECT 'course'                            as source,
                        course_id                          as id,
                        course_title                       as title,
                        course_title || ' ' || course_desc as description
                FROM course),
    departments AS (SELECT 'department'     as source,
                           department_id    as id,
                           department_title as title,
                           department_title as description
                    FROM department),
    persons AS (SELECT 'person'                       as source,
                       person_id                      as id,
                       first_name||' '||last_name     as title,
                       first_name||' '||patronymic||' '||last_name||' '||phone||' '||email
                         ||' '||skype||' '||nick_name as description
                FROM person)
SELECT * FROM courses
UNION
SELECT * FROM departments
UNION
SELECT * FROM persons;
