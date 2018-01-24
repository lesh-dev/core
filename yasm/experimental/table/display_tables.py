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
])
School = EasyTable(cols=[
    db.School.sch
])
PersonSchool = EasyTable(cols=[])
PersonComment = EasyTable(cols=[])
Submission = EasyTable(cols=[])
Contestants = EasyTable(cols=[])
Problems = EasyTable(cols=[])
Solutions = EasyTable(cols=[])