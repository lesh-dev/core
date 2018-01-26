from . import EasyTable
from yasm import db


NotificationDisplay = EasyTable(cols=[
    db.Notification.mail_group
])


DepartmentDisplay = EasyTable(cols=[
    db.Department.department_title
])


PersonDisplay = EasyTable(cols=[
    db.Person.first_name,
    db.Person.last_name,
    db.Person.nick_name
])


CourseDisplay = EasyTable(cols=[
    db.Course.course_title,
    db.Course.school_id
])


CourseTeachersDisplay = EasyTable(cols=[
    db.CourseTeachers.course_id,
    db.CourseTeachers.course_teachers_id
])


Exam = EasyTable(cols=[
    db.Exam.course_id,
    db.Exam.student_person_id
])


School = EasyTable(cols=[
    db.School.school_title
])


PersonSchool = EasyTable(cols=[
    db.PersonSchool.member_person_id,
    db.PersonSchool.member_department_id,
    db.PersonSchool.school_id
])


PersonComment = EasyTable(cols=[
    db.PersonComment.blamed_person_id,
    db.PersonComment.person_comment_created
])


Submission = EasyTable(cols=[
    db.Submission.sender,
    db.Submission.submission_timestamp
])


Contestants = EasyTable(cols=[
    db.Contestants.name,
    db.Contestants.contest_year
])


Problems = EasyTable(cols=[
    db.Problems.problem_name,
    db.Problems.contest_year
])


Solutions = EasyTable(cols=[
    db.Solutions.problem_id,
    db.Solutions.contestant_id,
    db.Solutions.resolution_author,
    db.Solutions.resolution_mark
])