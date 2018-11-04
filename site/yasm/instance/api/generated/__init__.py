from flask import Blueprint, jsonify, request
import instance.database
from flask_login import login_required
from instance.rights_decorator import has_rights

module = Blueprint('api', __name__, url_prefix='/api')


@module.route("/notification_list", methods=['GET'])
@has_rights('admin')
@login_required
def notification_list(req=None):
    regular = [
        'notification_id',
        'mail_group',
        'notification_text',
        'notification_html',
    ]
    field = {
        'notification_id': instance.database.Notification.notification_id,
        'mail_group': instance.database.Notification.mail_group,
        'notification_text': instance.database.Notification.notification_text,
        'notification_html': instance.database.Notification.notification_html,
    }
    query = instance.database.Notification.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/department_list", methods=['GET'])
@has_rights('admin')
@login_required
def department_list(req=None):
    regular = [
        'department_id',
        'department_title',
        'department_created',
        'department_modified',
        'department_changedby',
    ]
    field = {
        'department_id': instance.database.Department.department_id,
        'department_title': instance.database.Department.department_title,
        'department_created': instance.database.Department.department_created,
        'department_modified': instance.database.Department.department_modified,
        'department_changedby': instance.database.Department.department_changedby,
    }
    query = instance.database.Department.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/person_list", methods=['GET'])
@has_rights('admin')
@login_required
def person_list(req=None):
    regular = [
        'person_id',
        'rights',
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
    field = {
        'person_id': instance.database.Person.person_id,
        'rights': instance.database.Person.rights,
        'last_name': instance.database.Person.last_name,
        'first_name': instance.database.Person.first_name,
        'patronymic': instance.database.Person.patronymic,
        'nick_name': instance.database.Person.nick_name,
        'birth_date': instance.database.Person.birth_date,
        'passport_data': instance.database.Person.passport_data,
        'school': instance.database.Person.school,
        'school_city': instance.database.Person.school_city,
        'ank_class': instance.database.Person.ank_class,
        'current_class': instance.database.Person.current_class,
        'phone': instance.database.Person.phone,
        'cellular': instance.database.Person.cellular,
        'email': instance.database.Person.email,
        'skype': instance.database.Person.skype,
        'social_profile': instance.database.Person.social_profile,
        'is_teacher': instance.database.Person.is_teacher,
        'is_student': instance.database.Person.is_student,
        'favourites': instance.database.Person.favourites,
        'achievements': instance.database.Person.achievements,
        'hobby': instance.database.Person.hobby,
        'lesh_ref': instance.database.Person.lesh_ref,
        'forest_1': instance.database.Person.forest_1,
        'forest_2': instance.database.Person.forest_2,
        'forest_3': instance.database.Person.forest_3,
        'tent_capacity': instance.database.Person.tent_capacity,
        'tour_requisites': instance.database.Person.tour_requisites,
        'anketa_status': instance.database.Person.anketa_status,
        'user_agent': instance.database.Person.user_agent,
        'department_id': instance.database.Person.department_id,
        'person_created': instance.database.Person.person_created,
        'person_modified': instance.database.Person.person_modified,
        'person_changedby': instance.database.Person.person_changedby,
    }
    query = instance.database.Person.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/direct_login_list", methods=['GET'])
@has_rights('admin')
@login_required
def direct_login_list(req=None):
    regular = [
        'person_id',
        'login',
        'password_hash',
    ]
    field = {
        'person_id': instance.database.DirectLogin.person_id,
        'login': instance.database.DirectLogin.login,
        'password_hash': instance.database.DirectLogin.password_hash,
    }
    query = instance.database.DirectLogin.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/contact_list", methods=['GET'])
@has_rights('admin')
@login_required
def contact_list(req=None):
    regular = [
        'id',
        'person_id',
        'name',
        'value',
    ]
    field = {
        'id': instance.database.Contact.id,
        'person_id': instance.database.Contact.person_id,
        'name': instance.database.Contact.name,
        'value': instance.database.Contact.value,
    }
    query = instance.database.Contact.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/school_list", methods=['GET'])
@has_rights('admin')
@login_required
def school_list(req=None):
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
    field = {
        'school_id': instance.database.School.school_id,
        'school_title': instance.database.School.school_title,
        'school_type': instance.database.School.school_type,
        'school_date_start': instance.database.School.school_date_start,
        'school_date_end': instance.database.School.school_date_end,
        'school_location': instance.database.School.school_location,
        'school_coords': instance.database.School.school_coords,
        'school_created': instance.database.School.school_created,
        'school_modified': instance.database.School.school_modified,
        'school_changedby': instance.database.School.school_changedby,
    }
    query = instance.database.School.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/course_list", methods=['GET'])
@has_rights('admin')
@login_required
def course_list(req=None):
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
    field = {
        'course_id': instance.database.Course.course_id,
        'course_title': instance.database.Course.course_title,
        'school_id': instance.database.Course.school_id,
        'course_cycle': instance.database.Course.course_cycle,
        'target_class': instance.database.Course.target_class,
        'course_desc': instance.database.Course.course_desc,
        'course_type': instance.database.Course.course_type,
        'course_area': instance.database.Course.course_area,
        'course_comment': instance.database.Course.course_comment,
        'course_created': instance.database.Course.course_created,
        'course_modified': instance.database.Course.course_modified,
        'course_changedby': instance.database.Course.course_changedby,
    }
    query = instance.database.Course.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/course_teachers_list", methods=['GET'])
@has_rights('admin')
@login_required
def course_teachers_list(req=None):
    regular = [
        'course_teachers_id',
        'course_id',
        'course_teacher_id',
        'course_teachers_created',
        'course_teachers_modified',
        'course_teachers_changedby',
    ]
    field = {
        'course_teachers_id': instance.database.CourseTeachers.course_teachers_id,
        'course_id': instance.database.CourseTeachers.course_id,
        'course_teacher_id': instance.database.CourseTeachers.course_teacher_id,
        'course_teachers_created': instance.database.CourseTeachers.course_teachers_created,
        'course_teachers_modified': instance.database.CourseTeachers.course_teachers_modified,
        'course_teachers_changedby': instance.database.CourseTeachers.course_teachers_changedby,
    }
    query = instance.database.CourseTeachers.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/exam_list", methods=['GET'])
@has_rights('admin')
@login_required
def exam_list(req=None):
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
    field = {
        'exam_id': instance.database.Exam.exam_id,
        'student_person_id': instance.database.Exam.student_person_id,
        'course_id': instance.database.Exam.course_id,
        'exam_status': instance.database.Exam.exam_status,
        'deadline_date': instance.database.Exam.deadline_date,
        'exam_comment': instance.database.Exam.exam_comment,
        'exam_created': instance.database.Exam.exam_created,
        'exam_modified': instance.database.Exam.exam_modified,
        'exam_changedby': instance.database.Exam.exam_changedby,
    }
    query = instance.database.Exam.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/person_school_list", methods=['GET'])
@has_rights('admin')
@login_required
def person_school_list(req=None):
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
    field = {
        'person_school_id': instance.database.PersonSchool.person_school_id,
        'member_person_id': instance.database.PersonSchool.member_person_id,
        'member_department_id': instance.database.PersonSchool.member_department_id,
        'school_id': instance.database.PersonSchool.school_id,
        'is_student': instance.database.PersonSchool.is_student,
        'is_teacher': instance.database.PersonSchool.is_teacher,
        'curatorship': instance.database.PersonSchool.curatorship,
        'curator_group': instance.database.PersonSchool.curator_group,
        'current_class': instance.database.PersonSchool.current_class,
        'courses_needed': instance.database.PersonSchool.courses_needed,
        'person_school_comment': instance.database.PersonSchool.person_school_comment,
        'person_school_created': instance.database.PersonSchool.person_school_created,
        'person_school_modified': instance.database.PersonSchool.person_school_modified,
        'person_school_changedby': instance.database.PersonSchool.person_school_changedby,
        'frm': instance.database.PersonSchool.frm,
        'tll': instance.database.PersonSchool.tll,
    }
    query = instance.database.PersonSchool.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/person_comment_list", methods=['GET'])
@has_rights('admin')
@login_required
def person_comment_list(req=None):
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
    field = {
        'person_comment_id': instance.database.PersonComment.person_comment_id,
        'comment_text': instance.database.PersonComment.comment_text,
        'blamed_person_id': instance.database.PersonComment.blamed_person_id,
        'school_id': instance.database.PersonComment.school_id,
        'owner_login': instance.database.PersonComment.owner_login,
        'record_acl': instance.database.PersonComment.record_acl,
        'person_comment_created': instance.database.PersonComment.person_comment_created,
        'person_comment_modified': instance.database.PersonComment.person_comment_modified,
        'person_comment_deleted': instance.database.PersonComment.person_comment_deleted,
        'person_comment_changedby': instance.database.PersonComment.person_comment_changedby,
    }
    query = instance.database.PersonComment.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/submission_list", methods=['GET'])
@has_rights('admin')
@login_required
def submission_list(req=None):
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
    field = {
        'submission_id': instance.database.Submission.submission_id,
        'mail': instance.database.Submission.mail,
        'attachment': instance.database.Submission.attachment,
        'fileexchange': instance.database.Submission.fileexchange,
        'submission_timestamp': instance.database.Submission.submission_timestamp,
        'sender': instance.database.Submission.sender,
        'replied': instance.database.Submission.replied,
        'processed': instance.database.Submission.processed,
        'contest_year': instance.database.Submission.contest_year,
    }
    query = instance.database.Submission.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/contestants_list", methods=['GET'])
@has_rights('admin')
@login_required
def contestants_list(req=None):
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
    field = {
        'contestants_id': instance.database.Contestants.contestants_id,
        'name': instance.database.Contestants.name,
        'mail': instance.database.Contestants.mail,
        'phone': instance.database.Contestants.phone,
        'parents': instance.database.Contestants.parents,
        'address': instance.database.Contestants.address,
        'school': instance.database.Contestants.school,
        'level': instance.database.Contestants.level,
        'teacher_name': instance.database.Contestants.teacher_name,
        'work': instance.database.Contestants.work,
        'fileexchange': instance.database.Contestants.fileexchange,
        'status': instance.database.Contestants.status,
        'contest_year': instance.database.Contestants.contest_year,
    }
    query = instance.database.Contestants.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/problems_list", methods=['GET'])
@has_rights('admin')
@login_required
def problems_list(req=None):
    regular = [
        'problems_id',
        'contest_year',
        'problem_name',
        'problem_html',
        'people',
        'criteria',
    ]
    field = {
        'problems_id': instance.database.Problems.problems_id,
        'contest_year': instance.database.Problems.contest_year,
        'problem_name': instance.database.Problems.problem_name,
        'problem_html': instance.database.Problems.problem_html,
        'people': instance.database.Problems.people,
        'criteria': instance.database.Problems.criteria,
    }
    query = instance.database.Problems.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })


@module.route("/solutions_list", methods=['GET'])
@has_rights('admin')
@login_required
def solutions_list(req=None):
    regular = [
        'solutions_id',
        'problem_id',
        'contest_year',
        'contestant_id',
        'resolution_text',
        'resolution_author',
        'resolution_mark',
    ]
    field = {
        'solutions_id': instance.database.Solutions.solutions_id,
        'problem_id': instance.database.Solutions.problem_id,
        'contest_year': instance.database.Solutions.contest_year,
        'contestant_id': instance.database.Solutions.contestant_id,
        'resolution_text': instance.database.Solutions.resolution_text,
        'resolution_author': instance.database.Solutions.resolution_author,
        'resolution_mark': instance.database.Solutions.resolution_mark,
    }
    query = instance.database.Solutions.query
    col = request.args.items() if req is None else req.items()
    for arg, val in col:
        if arg in regular:
            query = query.filter(field[arg] == val)
    query = query.all()
    ans = []
    for entry in query:
        ans.append(entry.serialize())
    return jsonify({
        'length': len(ans),
        'values': ans
    })
