from flask import Blueprint, jsonify, request
from instance.database import *
from flask_login import login_required

module = Blueprint('api', __name__, url_prefix='/api')


@login_required
@module.route("/users_list", methods=['GET'])
def users_list(req=None, raw=False):
    regular = [
        'id',
        'social_id',
        'nickname',
        'email',
    ]
    additional = {
    }
    field = {
        'id': User.id,
        'social_id': User.social_id,
        'nickname': User.nickname,
        'email': User.email,
    }
    query = User.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/notification_list", methods=['GET'])
def notification_list(req=None, raw=False):
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/department_list", methods=['GET'])
def department_list(req=None, raw=False):
    regular = [
        'department_id',
        'department_title',
        'department_created',
        'department_modified',
        'department_changedby',
    ]
    additional = {
        'person_list': {'length': 0, 'values': []},
        'person_school_list': {'length': 0, 'values': []},
    }
    field = {
        'department_id': Department.department_id,
        'department_title': Department.department_title,
        'department_created': Department.department_created,
        'department_modified': Department.department_modified,
        'department_changedby': Department.department_changedby,
    }
    query = Department.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/person_list", methods=['GET'])
def person_list(req=None, raw=False):
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
        'contact_list': {'length': 0, 'values': []},
        'course_teachers_list': {'length': 0, 'values': []},
        'exam_list': {'length': 0, 'values': []},
        'person_school_list': {'length': 0, 'values': []},
        'person_comment_list': {'length': 0, 'values': []},
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['department_id_fk'] = department_list(req={'department_id': entry.department_id}, raw=True)['values']
        d['department_id_fk'] = d['department_id_fk'][0] if len(d['department_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/contact_list", methods=['GET'])
def contact_list(req=None, raw=False):
    regular = [
        'id',
        'person_id',
        'name',
        'value',
    ]
    additional = {
    }
    field = {
        'id': Contact.id,
        'person_id': Contact.person_id,
        'name': Contact.name,
        'value': Contact.value,
    }
    query = Contact.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['person_id_fk'] = person_list(req={'person_id': entry.person_id}, raw=True)['values']
        d['person_id_fk'] = d['person_id_fk'][0] if len(d['person_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/school_list", methods=['GET'])
def school_list(req=None, raw=False):
    regular = [
        'school_id',
        'school_title',
        'school_type',
        'school_date_start',
        'school_date_end',
        'school_location',
        'school_coords',
        'school_created',
        'school_modified',
        'school_changedby',
    ]
    additional = {
        'course_list': {'length': 0, 'values': []},
        'person_school_list': {'length': 0, 'values': []},
        'person_comment_list': {'length': 0, 'values': []},
    }
    field = {
        'school_id': School.school_id,
        'school_title': School.school_title,
        'school_type': School.school_type,
        'school_date_start': School.school_date_start,
        'school_date_end': School.school_date_end,
        'school_location': School.school_location,
        'school_coords': School.school_coords,
        'school_created': School.school_created,
        'school_modified': School.school_modified,
        'school_changedby': School.school_changedby,
    }
    query = School.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/course_list", methods=['GET'])
def course_list(req=None, raw=False):
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
        'course_teachers_list': {'length': 0, 'values': []},
        'exam_list': {'length': 0, 'values': []},
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['school_id_fk'] = school_list(req={'school_id': entry.school_id}, raw=True)['values']
        d['school_id_fk'] = d['school_id_fk'][0] if len(d['school_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/course_teachers_list", methods=['GET'])
def course_teachers_list(req=None, raw=False):
    regular = [
        'course_teachers_id',
        'course_id',
        'course_teacher_id',
        'course_teachers_created',
        'course_teachers_modified',
        'course_teachers_changedby',
    ]
    additional = {
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['course_id_fk'] = course_list(req={'course_id': entry.course_id}, raw=True)['values']
        d['course_id_fk'] = d['course_id_fk'][0] if len(d['course_id_fk']) else None
        d['course_teacher_id_fk'] = person_list(req={'person_id': entry.course_teacher_id}, raw=True)['values']
        d['course_teacher_id_fk'] = d['course_teacher_id_fk'][0] if len(d['course_teacher_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/exam_list", methods=['GET'])
def exam_list(req=None, raw=False):
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['student_person_id_fk'] = person_list(req={'person_id': entry.student_person_id}, raw=True)['values']
        d['student_person_id_fk'] = d['student_person_id_fk'][0] if len(d['student_person_id_fk']) else None
        d['course_id_fk'] = course_list(req={'course_id': entry.course_id}, raw=True)['values']
        d['course_id_fk'] = d['course_id_fk'][0] if len(d['course_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/person_school_list", methods=['GET'])
def person_school_list(req=None, raw=False):
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
        'frm',
        'tll',
    ]
    additional = {
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
        'frm': PersonSchool.frm,
        'tll': PersonSchool.tll,
    }
    query = PersonSchool.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['member_person_id_fk'] = person_list(req={'person_id': entry.member_person_id}, raw=True)['values']
        d['member_person_id_fk'] = d['member_person_id_fk'][0] if len(d['member_person_id_fk']) else None
        d['member_department_id_fk'] = department_list(req={'department_id': entry.member_department_id}, raw=True)['values']
        d['member_department_id_fk'] = d['member_department_id_fk'][0] if len(d['member_department_id_fk']) else None
        d['school_id_fk'] = school_list(req={'school_id': entry.school_id}, raw=True)['values']
        d['school_id_fk'] = d['school_id_fk'][0] if len(d['school_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/person_comment_list", methods=['GET'])
def person_comment_list(req=None, raw=False):
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['blamed_person_id_fk'] = person_list(req={'person_id': entry.blamed_person_id}, raw=True)['values']
        d['blamed_person_id_fk'] = d['blamed_person_id_fk'][0] if len(d['blamed_person_id_fk']) else None
        d['school_id_fk'] = school_list(req={'school_id': entry.school_id}, raw=True)['values']
        d['school_id_fk'] = d['school_id_fk'][0] if len(d['school_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/submission_list", methods=['GET'])
def submission_list(req=None, raw=False):
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/contestants_list", methods=['GET'])
def contestants_list(req=None, raw=False):
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
        'solutions_list': {'length': 0, 'values': []},
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/problems_list", methods=['GET'])
def problems_list(req=None, raw=False):
    regular = [
        'problems_id',
        'contest_year',
        'problem_name',
        'problem_html',
        'people',
        'criteria',
    ]
    additional = {
        'solutions_list': {'length': 0, 'values': []},
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@login_required
@module.route("/solutions_list", methods=['GET'])
def solutions_list(req=None, raw=False):
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
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        d = dict()
        d['problem_id_fk'] = problems_list(req={'problems_id': entry.problem_id}, raw=True)['values']
        d['problem_id_fk'] = d['problem_id_fk'][0] if len(d['problem_id_fk']) else None
        d['contestant_id_fk'] = contestants_list(req={'contestants_id': entry.contestant_id}, raw=True)['values']
        d['contestant_id_fk'] = d['contestant_id_fk'][0] if len(d['contestant_id_fk']) else None
        d.update(entry.__dict__)
        d.pop('_sa_instance_state')
        d.update(additional)
        ans.append(d)
    if raw:
        return {
            'length': len(ans),
            'values': ans
        }
    return jsonify({
        'length': len(ans),
        'values': ans
    })


