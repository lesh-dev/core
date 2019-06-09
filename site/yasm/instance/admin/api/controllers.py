"""
.. _admin_api_controllers:

Url dispatching file of :ref:`admin_api <admin_api>` module

|contains|
 * module - :ref:`nestable blueprint <nestable_blueprint>` which represents admin.api module of YaSM
"""
from flask import request as rq, Response, jsonify
from instance.database import db, School, Contact, Person
from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('admin_api', __name__, url_prefix='/api')


def resp(code, data):
    """
    Forms response out of status code and data

    :param code: response code

    :param data: data to be translated to

    :return: Response with JSON formatted data and response code
    """
    return Response(
        status=code,
        mimetype="application/json",
        response=jsonify(data)
    )


@module.route('/schools/add', methods=['POST'])
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


@module.route('/person/contact/del/<int:id>', methods=['POST'])
def api_person_contact_del(id):
    Contact.query.filter(Contact.id == id).delete()
    db.session.commit()
    return jsonify('OK')


@module.route('/person/contact/add/<int:person_id>', methods=['POST'])
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


@module.route('/person/department/change/<int:person_id>', methods=['POST'])
def api_person_department_change(person_id):
    id = rq.values['department_id']
    Person.query.filter(Person.person_id == person_id).update({'department_id': id})
    db.session.commit()
    return jsonify('OK')
