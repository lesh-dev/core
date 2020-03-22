from flask import jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import enum
import time

from instance.NestableBlueprint import NestableBlueprint
from instance.database import Ava, Contact, Course, CourseTeachers, EntryStates, Person, db, search_all

module = NestableBlueprint('internal-api', __name__, url_prefix='/api')

@module.route('/search', methods=['POST'])
@login_required
def search():
    return jsonify({
        'payload': list(search_all(request.json['query'], request.json.get('tables', None))),
        'query': request.json['query'],
    })


@module.route('/patch_teachers', methods=['POST'])
@login_required
def patch_teachers():
    course = Course.query.get(int(request.json['id']))
    if course is None:
        return jsonify({})
    course_teachers = course.course_teachers.all()
    new_teachers = []
    for pid, spec in request.json['patch'].items():
        action = spec['action']
        if action == PatchActions.Remove.value:
            for link in course_teachers:
                pass

    for contact in new_contacts:
        db.session.add(contact)
    db.session.commit()
    return jsonify(
        [
            # contact.serialize()
            # for contact in current_user.contacts.all()
        ]
    )