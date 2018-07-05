from flask import Blueprint, jsonify, request
from ..database import *

module = Blueprint('api', __name__, url_prefix='/api')


@module.route("/notification_list", methods=['GET'])
def notification_list():
    regular = [
        'notification_id',
        'mail_group',
        'notification_text',
        'notification_html',
    ]
    additional = {
    }
    field = {
        'notification_id': Notification.notification_id,
        'mail_group': Notification.mail_group,
        'notification_text': Notification.notification_text,
        'notification_html': Notification.notification_html,
    }
    query = Notification.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['notification_id'] = entry.notification_id
        d['mail_group'] = entry.mail_group
        d['notification_text'] = entry.notification_text
        d['notification_html'] = entry.notification_html
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/department_list", methods=['GET'])
def department_list():
    regular = [
        'department_id',
        'department_title',
        'department_created',
        'department_modified',
        'department_changedby',
    ]
    additional = {
        'person_list': [],
        'person_school_list': [],
    }
    field = {
        'department_id': Department.department_id,
        'department_title': Department.department_title,
        'department_created': Department.department_created,
        'department_modified': Department.department_modified,
        'department_changedby': Department.department_changedby,
    }
    query = Department.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['department_id'] = entry.department_id
        d['department_title'] = entry.department_title
        d['department_created'] = entry.department_created
        d['department_modified'] = entry.department_modified
        d['department_changedby'] = entry.department_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/person_list", methods=['GET'])
def person_list():
    regular = [
        'person_id',
        'last_name',
        'first_name',
        'patronymic',
        'nick_name',
        'birth_date',
        'passport_data',
        'school',
        'school_city',
        'ank_class',
        'current_class',
        'phone',
        'cellular',
        'email',
        'skype',
        'social_profile',
        'is_teacher',
        'is_student',
        'favourites',
        'achievements',
        'hobby',
        'lesh_ref',
        'forest_1',
        'forest_2',
        'forest_3',
        'tent_capacity',
        'tour_requisites',
        'anketa_status',
        'user_agent',
        'department_id',
        'person_created',
        'person_modified',
        'person_changedby',
    ]
    additional = {
        'department': [],
        'course_teachers_list': [],
        'exam_list': [],
        'person_school_list': [],
        'person_comment_list': [],
    }
    field = {
        'person_id': Person.person_id,
        'last_name': Person.last_name,
        'first_name': Person.first_name,
        'patronymic': Person.patronymic,
        'nick_name': Person.nick_name,
        'birth_date': Person.birth_date,
        'passport_data': Person.passport_data,
        'school': Person.school,
        'school_city': Person.school_city,
        'ank_class': Person.ank_class,
        'current_class': Person.current_class,
        'phone': Person.phone,
        'cellular': Person.cellular,
        'email': Person.email,
        'skype': Person.skype,
        'social_profile': Person.social_profile,
        'is_teacher': Person.is_teacher,
        'is_student': Person.is_student,
        'favourites': Person.favourites,
        'achievements': Person.achievements,
        'hobby': Person.hobby,
        'lesh_ref': Person.lesh_ref,
        'forest_1': Person.forest_1,
        'forest_2': Person.forest_2,
        'forest_3': Person.forest_3,
        'tent_capacity': Person.tent_capacity,
        'tour_requisites': Person.tour_requisites,
        'anketa_status': Person.anketa_status,
        'user_agent': Person.user_agent,
        'department_id': Person.department_id,
        'person_created': Person.person_created,
        'person_modified': Person.person_modified,
        'person_changedby': Person.person_changedby,
    }
    query = Person.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['person_id'] = entry.person_id
        d['last_name'] = entry.last_name
        d['first_name'] = entry.first_name
        d['patronymic'] = entry.patronymic
        d['nick_name'] = entry.nick_name
        d['birth_date'] = entry.birth_date
        d['passport_data'] = entry.passport_data
        d['school'] = entry.school
        d['school_city'] = entry.school_city
        d['ank_class'] = entry.ank_class
        d['current_class'] = entry.current_class
        d['phone'] = entry.phone
        d['cellular'] = entry.cellular
        d['email'] = entry.email
        d['skype'] = entry.skype
        d['social_profile'] = entry.social_profile
        d['is_teacher'] = entry.is_teacher
        d['is_student'] = entry.is_student
        d['favourites'] = entry.favourites
        d['achievements'] = entry.achievements
        d['hobby'] = entry.hobby
        d['lesh_ref'] = entry.lesh_ref
        d['forest_1'] = entry.forest_1
        d['forest_2'] = entry.forest_2
        d['forest_3'] = entry.forest_3
        d['tent_capacity'] = entry.tent_capacity
        d['tour_requisites'] = entry.tour_requisites
        d['anketa_status'] = entry.anketa_status
        d['user_agent'] = entry.user_agent
        d['department_id'] = entry.department_id
        d['person_created'] = entry.person_created
        d['person_modified'] = entry.person_modified
        d['person_changedby'] = entry.person_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/course_list", methods=['GET'])
def course_list():
    regular = [
        'course_id',
        'course_title',
        'school_id',
        'course_cycle',
        'target_class',
        'course_desc',
        'course_type',
        'course_area',
        'course_comment',
        'course_created',
        'course_modified',
        'course_changedby',
    ]
    additional = {
        'course_teachers_list': [],
        'exam_list': [],
    }
    field = {
        'course_id': Course.course_id,
        'course_title': Course.course_title,
        'school_id': Course.school_id,
        'course_cycle': Course.course_cycle,
        'target_class': Course.target_class,
        'course_desc': Course.course_desc,
        'course_type': Course.course_type,
        'course_area': Course.course_area,
        'course_comment': Course.course_comment,
        'course_created': Course.course_created,
        'course_modified': Course.course_modified,
        'course_changedby': Course.course_changedby,
    }
    query = Course.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['course_id'] = entry.course_id
        d['course_title'] = entry.course_title
        d['school_id'] = entry.school_id
        d['course_cycle'] = entry.course_cycle
        d['target_class'] = entry.target_class
        d['course_desc'] = entry.course_desc
        d['course_type'] = entry.course_type
        d['course_area'] = entry.course_area
        d['course_comment'] = entry.course_comment
        d['course_created'] = entry.course_created
        d['course_modified'] = entry.course_modified
        d['course_changedby'] = entry.course_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/course_teachers_list", methods=['GET'])
def course_teachers_list():
    regular = [
        'course_teachers_id',
        'course_id',
        'course_teacher_id',
        'course_teachers_created',
        'course_teachers_modified',
        'course_teachers_changedby',
    ]
    additional = {
        'course': [],
        'person': [],
    }
    field = {
        'course_teachers_id': CourseTeachers.course_teachers_id,
        'course_id': CourseTeachers.course_id,
        'course_teacher_id': CourseTeachers.course_teacher_id,
        'course_teachers_created': CourseTeachers.course_teachers_created,
        'course_teachers_modified': CourseTeachers.course_teachers_modified,
        'course_teachers_changedby': CourseTeachers.course_teachers_changedby,
    }
    query = CourseTeachers.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['course_teachers_id'] = entry.course_teachers_id
        d['course_id'] = entry.course_id
        d['course_teacher_id'] = entry.course_teacher_id
        d['course_teachers_created'] = entry.course_teachers_created
        d['course_teachers_modified'] = entry.course_teachers_modified
        d['course_teachers_changedby'] = entry.course_teachers_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/exam_list", methods=['GET'])
def exam_list():
    regular = [
        'exam_id',
        'student_person_id',
        'course_id',
        'exam_status',
        'deadline_date',
        'exam_comment',
        'exam_created',
        'exam_modified',
        'exam_changedby',
    ]
    additional = {
        'person': [],
        'course': [],
    }
    field = {
        'exam_id': Exam.exam_id,
        'student_person_id': Exam.student_person_id,
        'course_id': Exam.course_id,
        'exam_status': Exam.exam_status,
        'deadline_date': Exam.deadline_date,
        'exam_comment': Exam.exam_comment,
        'exam_created': Exam.exam_created,
        'exam_modified': Exam.exam_modified,
        'exam_changedby': Exam.exam_changedby,
    }
    query = Exam.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['exam_id'] = entry.exam_id
        d['student_person_id'] = entry.student_person_id
        d['course_id'] = entry.course_id
        d['exam_status'] = entry.exam_status
        d['deadline_date'] = entry.deadline_date
        d['exam_comment'] = entry.exam_comment
        d['exam_created'] = entry.exam_created
        d['exam_modified'] = entry.exam_modified
        d['exam_changedby'] = entry.exam_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/school_list", methods=['GET'])
def school_list():
    regular = [
        'school_id',
        'school_title',
        'school_type',
        'school_date_start',
        'school_date_end',
        'school_location',
        'school_created',
        'school_modified',
        'school_changedby',
    ]
    additional = {
        'person_school_list': [],
        'person_comment_list': [],
    }
    field = {
        'school_id': School.school_id,
        'school_title': School.school_title,
        'school_type': School.school_type,
        'school_date_start': School.school_date_start,
        'school_date_end': School.school_date_end,
        'school_location': School.school_location,
        'school_created': School.school_created,
        'school_modified': School.school_modified,
        'school_changedby': School.school_changedby,
    }
    query = School.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['school_id'] = entry.school_id
        d['school_title'] = entry.school_title
        d['school_type'] = entry.school_type
        d['school_date_start'] = entry.school_date_start
        d['school_date_end'] = entry.school_date_end
        d['school_location'] = entry.school_location
        d['school_created'] = entry.school_created
        d['school_modified'] = entry.school_modified
        d['school_changedby'] = entry.school_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/person_school_list", methods=['GET'])
def person_school_list():
    regular = [
        'person_school_id',
        'member_person_id',
        'member_department_id',
        'school_id',
        'is_student',
        'is_teacher',
        'curatorship',
        'curator_group',
        'current_class',
        'courses_needed',
        'person_school_comment',
        'person_school_created',
        'person_school_modified',
        'person_school_changedby',
    ]
    additional = {
        'person': [],
        'department': [],
        'school': [],
    }
    field = {
        'person_school_id': PersonSchool.person_school_id,
        'member_person_id': PersonSchool.member_person_id,
        'member_department_id': PersonSchool.member_department_id,
        'school_id': PersonSchool.school_id,
        'is_student': PersonSchool.is_student,
        'is_teacher': PersonSchool.is_teacher,
        'curatorship': PersonSchool.curatorship,
        'curator_group': PersonSchool.curator_group,
        'current_class': PersonSchool.current_class,
        'courses_needed': PersonSchool.courses_needed,
        'person_school_comment': PersonSchool.person_school_comment,
        'person_school_created': PersonSchool.person_school_created,
        'person_school_modified': PersonSchool.person_school_modified,
        'person_school_changedby': PersonSchool.person_school_changedby,
    }
    query = PersonSchool.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['person_school_id'] = entry.person_school_id
        d['member_person_id'] = entry.member_person_id
        d['member_department_id'] = entry.member_department_id
        d['school_id'] = entry.school_id
        d['is_student'] = entry.is_student
        d['is_teacher'] = entry.is_teacher
        d['curatorship'] = entry.curatorship
        d['curator_group'] = entry.curator_group
        d['current_class'] = entry.current_class
        d['courses_needed'] = entry.courses_needed
        d['person_school_comment'] = entry.person_school_comment
        d['person_school_created'] = entry.person_school_created
        d['person_school_modified'] = entry.person_school_modified
        d['person_school_changedby'] = entry.person_school_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/person_comment_list", methods=['GET'])
def person_comment_list():
    regular = [
        'person_comment_id',
        'comment_text',
        'blamed_person_id',
        'school_id',
        'owner_login',
        'record_acl',
        'person_comment_created',
        'person_comment_modified',
        'person_comment_deleted',
        'person_comment_changedby',
    ]
    additional = {
        'person': [],
        'school': [],
    }
    field = {
        'person_comment_id': PersonComment.person_comment_id,
        'comment_text': PersonComment.comment_text,
        'blamed_person_id': PersonComment.blamed_person_id,
        'school_id': PersonComment.school_id,
        'owner_login': PersonComment.owner_login,
        'record_acl': PersonComment.record_acl,
        'person_comment_created': PersonComment.person_comment_created,
        'person_comment_modified': PersonComment.person_comment_modified,
        'person_comment_deleted': PersonComment.person_comment_deleted,
        'person_comment_changedby': PersonComment.person_comment_changedby,
    }
    query = PersonComment.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['person_comment_id'] = entry.person_comment_id
        d['comment_text'] = entry.comment_text
        d['blamed_person_id'] = entry.blamed_person_id
        d['school_id'] = entry.school_id
        d['owner_login'] = entry.owner_login
        d['record_acl'] = entry.record_acl
        d['person_comment_created'] = entry.person_comment_created
        d['person_comment_modified'] = entry.person_comment_modified
        d['person_comment_deleted'] = entry.person_comment_deleted
        d['person_comment_changedby'] = entry.person_comment_changedby
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/submission_list", methods=['GET'])
def submission_list():
    regular = [
        'submission_id',
        'mail',
        'attachment',
        'fileexchange',
        'submission_timestamp',
        'sender',
        'replied',
        'processed',
        'contest_year',
    ]
    additional = {
    }
    field = {
        'submission_id': Submission.submission_id,
        'mail': Submission.mail,
        'attachment': Submission.attachment,
        'fileexchange': Submission.fileexchange,
        'submission_timestamp': Submission.submission_timestamp,
        'sender': Submission.sender,
        'replied': Submission.replied,
        'processed': Submission.processed,
        'contest_year': Submission.contest_year,
    }
    query = Submission.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['submission_id'] = entry.submission_id
        d['mail'] = entry.mail
        d['attachment'] = entry.attachment
        d['fileexchange'] = entry.fileexchange
        d['submission_timestamp'] = entry.submission_timestamp
        d['sender'] = entry.sender
        d['replied'] = entry.replied
        d['processed'] = entry.processed
        d['contest_year'] = entry.contest_year
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/contestants_list", methods=['GET'])
def contestants_list():
    regular = [
        'contestants_id',
        'name',
        'mail',
        'phone',
        'parents',
        'address',
        'school',
        'level',
        'teacher_name',
        'work',
        'fileexchange',
        'status',
        'contest_year',
    ]
    additional = {
        'solutions_list': [],
    }
    field = {
        'contestants_id': Contestants.contestants_id,
        'name': Contestants.name,
        'mail': Contestants.mail,
        'phone': Contestants.phone,
        'parents': Contestants.parents,
        'address': Contestants.address,
        'school': Contestants.school,
        'level': Contestants.level,
        'teacher_name': Contestants.teacher_name,
        'work': Contestants.work,
        'fileexchange': Contestants.fileexchange,
        'status': Contestants.status,
        'contest_year': Contestants.contest_year,
    }
    query = Contestants.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['contestants_id'] = entry.contestants_id
        d['name'] = entry.name
        d['mail'] = entry.mail
        d['phone'] = entry.phone
        d['parents'] = entry.parents
        d['address'] = entry.address
        d['school'] = entry.school
        d['level'] = entry.level
        d['teacher_name'] = entry.teacher_name
        d['work'] = entry.work
        d['fileexchange'] = entry.fileexchange
        d['status'] = entry.status
        d['contest_year'] = entry.contest_year
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/problems_list", methods=['GET'])
def problems_list():
    regular = [
        'problems_id',
        'contest_year',
        'problem_name',
        'problem_html',
        'people',
        'criteria',
    ]
    additional = {
        'solutions_list': [],
    }
    field = {
        'problems_id': Problems.problems_id,
        'contest_year': Problems.contest_year,
        'problem_name': Problems.problem_name,
        'problem_html': Problems.problem_html,
        'people': Problems.people,
        'criteria': Problems.criteria,
    }
    query = Problems.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['problems_id'] = entry.problems_id
        d['contest_year'] = entry.contest_year
        d['problem_name'] = entry.problem_name
        d['problem_html'] = entry.problem_html
        d['people'] = entry.people
        d['criteria'] = entry.criteria
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


@module.route("/solutions_list", methods=['GET'])
def solutions_list():
    regular = [
        'solutions_id',
        'problem_id',
        'contest_year',
        'contestant_id',
        'resolution_text',
        'resolution_author',
        'resolution_mark',
    ]
    additional = {
        'problems': [],
        'contestants': [],
    }
    field = {
        'solutions_id': Solutions.solutions_id,
        'problem_id': Solutions.problem_id,
        'contest_year': Solutions.contest_year,
        'contestant_id': Solutions.contestant_id,
        'resolution_text': Solutions.resolution_text,
        'resolution_author': Solutions.resolution_author,
        'resolution_mark': Solutions.resolution_mark,
    }
    query = Solutions.query
    for arg, val in request.args.items():
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['solutions_id'] = entry.solutions_id
        d['problem_id'] = entry.problem_id
        d['contest_year'] = entry.contest_year
        d['contestant_id'] = entry.contestant_id
        d['resolution_text'] = entry.resolution_text
        d['resolution_author'] = entry.resolution_author
        d['resolution_mark'] = entry.resolution_mark
        d.update(additional)
        ans.append(d)
    return jsonify(ans)


