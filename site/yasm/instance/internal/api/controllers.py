from flask import jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import enum
import time

from instance.NestableBlueprint import NestableBlueprint
from instance.database import Ava, Contact, Course, CourseTeachers, EntryStates, Person, db, search_all

module = NestableBlueprint('internal-api', __name__, url_prefix='/api')

class PatchActions(enum.Enum):
    Add = 0
    Remove = 1


@module.route('/get_profile', methods=['POST'])
@login_required
def get_profile():
    ava = current_user.avas.filter(Ava.entry_state == EntryStates.RELEVANT).one_or_none()

    return jsonify({
        'person_id': current_user.person_id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'nick_name': current_user.nick_name,
        'avas': [ava.serialize() if ava is not None else {}],
    })


@module.route('/set_ava', methods=['POST'])
@login_required
def set_ava():
    for ava in current_user.avas.filter(Ava.entry_state == EntryStates.RELEVANT).all():
        ava.entry_state = EntryStates.OUTDATED
    db.session.commit()
    ava = Ava(
        person=current_user,
        ava=request.json['new_ava']
    )
    db.session.add(ava)
    db.session.commit()
    return jsonify(ava.serialize())


@module.route('/patch_contacts', methods=['POST'])
@login_required
def patch_contacts():
    contacts = {
        c.value: c
        for c in current_user.contacts.all()
    }
    new_contacts = []
    for value, spec in request.json['patch'].items():
        if value in contacts:
            if spec['action'] == PatchActions.Add.value:
                contacts[value].name = spec['name']
            else:
                db.session.delete(contacts[value])
        else:
            if spec['action'] == PatchActions.Add.value:
                new_contacts.append(
                    Contact(
                        person=current_user,
                        name=spec['name'],
                        value=value,
                    )
                )
    for contact in new_contacts:
        db.session.add(contact)
    db.session.commit()
    return jsonify(
        [
            contact.serialize()
            for contact in current_user.contacts.all()
        ]
    )


@module.route('/get_profile_info', methods=['POST'])
@login_required
def get_profile_info():
    return jsonify(fill_person(current_user))


@module.route('/update_password', methods=['POST'])
@login_required
def update_password():
    current_user.direct_login.update(
        values={
            'password_hash': generate_password_hash(password=request.values['new_password'])
        }
    )
    return jsonify('OK')


@module.route('/courses', methods=['POST'])
@login_required
def courses():
    return jsonify(
        [ct.course.serialize() for ct in current_user.course_teachers]
    )


@module.route('/fetch_person', methods=['POST'])
@login_required
def person():
    return jsonify(fill_person(Person.query.get(int(request.json['id']))))


def fill_person(person):
    response = person.serialize()
    response['person_schools'] = [school.serialize() for school in person.person_schools.all()]
    response['exams'] = [school.serialize() for school in person.exams.all()]
    response['course_teachers'] = [school.serialize() for school in person.course_teachers.all()]
    response['contacts'] = [school.serialize() for school in person.contacts.all()]
    return response


@module.route('/search', methods=['POST'])
@login_required
def search():
    return jsonify({
        'payload': list(search_all(request.json['query'], request.json.get('tables', None))),
        'query': request.json['query'],
    })


@module.route('/fetch_course', methods=['POST'])
@login_required
def fetch_course():
    c = Course.query.get(int(request.json['id']))
    if c is None:
        return jsonify({})

    response = c.serialize()
    response['course_teachers'] = [ct.serialize() for ct in c.course_teachers.all()]
    response['exams'] = [e.serialize() for e in c.exams.all()]
    return jsonify(response)


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