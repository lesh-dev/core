select course.course_title, person.last_name || " " || person.first_name from
    course,
    person,
    school,
    course_teachers,
    person_school
    where
        school.school_title = "ЛЭШ-2014" and
        course.school_id = school.school_id and
        person_school.member_department_id = 1 and
        course_teachers.course_teacher_id = person.person_id and
        course.course_id = course_teachers.course_id and
        person_school.school_id = course.school_id and
        person.person_id = person_school.member_person_id;
