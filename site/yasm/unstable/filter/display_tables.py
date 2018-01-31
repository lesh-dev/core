import db


def get_display(cl):
    if db.Notification == cl:
        return {
            'id': cl.notification_id,
            'mail_group': cl.mail_group
        }
    elif db.Department == cl:
        return {
            'id': cl.department_id,
            'title': cl.department_title
        }
    elif db.Person == cl:
        return {
            'id': cl.person_id,
            'first_name': cl.first_name,
            'last_name': cl.last_name,
            'nick_name': cl.nick_name
        }
    elif db.Course == cl:
        return {
            'id': cl.course_id,
            'title': cl.course_title,
            'school': cl.school_id
        }
    elif db.CourseTeachers == cl:
        return {
            'id': cl.course_teachers_id,
            'course': cl.course_id,
            'teacher': cl.course_teachers_id
        }
    elif db.Exam == cl:
        return {
            'id': cl.exam_id,
            'course': cl.course_id,
            'student': cl.student_person_id
        }
    elif db.School == cl:
        return {
            'id': cl.school_id,
            'title': cl.school_title
        }
    elif db.PersonSchool == cl:
        return {
            'id': cl.person_school_id,
            'member': cl.member_person_id,
            'department': cl.member_department_id,
            'school': cl.school_id
        }
    elif db.PersonComment == cl:
        return {
            'id': cl.person_comment_id,
            'blamed': cl.blamed_person_id,
            'creator': cl.person_comment_created
        }
    elif db.Submission == cl:
        return {
            'id': cl.submission_id,
            'sender': cl.sender,
            'timestamp': cl.submission_timestamp
        }
    elif db.Contestants == cl:
        return {
            'id': cl.contestants_id,
            'name': cl.name,
            'year': cl.contest_year
        }
    elif db.Problems == cl:
        return {
            'id': cl.problem_id,
            'name': cl.problem_name,
            'year': cl.contest_year
        }
    elif db.Solutions == cl:
        return {
            'id': cl.solutions_id,
            'problem': cl.problem_id,
            'contestant': cl.contestant_id,
            'resolution': cl.resolution_mark
        }
    else:
        return {}