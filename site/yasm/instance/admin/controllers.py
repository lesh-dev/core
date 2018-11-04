from flask import render_template, redirect, request as rq, Response, jsonify
from flask_login import login_required, current_user
from ..menu import menu
from .side import side
from ..database import db, School, Contact, Person
from ..rights_decorator import has_rights
from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('admin', __name__, url_prefix='/admin')


def resp(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=jsonify(data)
    )


@module.route('/', methods=['GET'])
@login_required
@has_rights('admin')
def index():
    return render_template(
        "admin/base.html",
        menu=menu,
        person=current_user,
        side=side
    )


@module.route('/gui/', methods=['GET'])
@module.route('/gui/<path:path>', methods=['GET'])
@login_required
@has_rights('admin')
def admin(path='path'):  # resolved by reactJS
    return render_template(
        "admin/base.html",
        menu=menu,
        person=current_user,
        side=side
    )


@module.route('/api/schools/add', methods=['GET'])
@login_required
@has_rights('admin')
def school_add():
    args = rq.args
    title = args['title']
    start = args['start']
    end = args['end']
    tp = args['type']
    location = args['location']
    s = School(
        school_title=title,
        school_type=tp,
        school_date_start=start,
        school_date_end=end,
        school_location=location,
        school_created='now',
        school_modified='now',
        school_changedby='me'
    )
    db.session.add(s)
    db.session.commit()
    return resp(200, [])


@module.route('/api/person/contact/del/<int:id>', methods=['POST'])
@login_required
@has_rights('admin')
def api_person_contact_del(id):
    Contact.query.filter(Contact.id == id).delete()
    db.session.commit()
    return jsonify('OK')


@module.route('/api/person/contact/add/<int:person_id>', methods=['POST'])
@login_required
@has_rights('admin')
def api_person_contact_add(person_id):
    name = rq.values['name']
    url = rq.values['url']
    add = Contact(
        person_id=person_id,
        name=name,
        value=url
    )
    db.session.add(add)
    db.session.commit()
    return jsonify('OK')


@module.route('/api/person/department/change/<int:person_id>', methods=['POST'])
@login_required
@has_rights('admin')
def api_person_department_change(person_id):
    id = rq.values['department_id']
    Person.query.filter(Person.person_id == person_id).update({'department_id': id})
    db.session.commit()
    return jsonify('OK')
