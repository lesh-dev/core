#!/usr/bin/python

primary_keys = [
    "blamed_person_id",
    "course_id",
    "course_teacher_id",
    "course_teachers_id",
    "department_id",
    "exam_id",
    "member_department_id",
    "member_person_id",
    "person_comment_id",
    "person_id",
    "person_school_id",
    "school_id",
    "student_person_id",
]


tables = [
    "xversion",
    "department",
    "person",
    "course",
    "course_teachers",
    "exam",
    "school",
    "person_school",
    "person_comment",
]

for table in tables:
    for key in primary_keys:
        print "SELECT * FROM {table} WHERE {key} = -1;".format(table=table, key=key)
